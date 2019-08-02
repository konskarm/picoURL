# picoURL

## Problem analysis
Shortening a URL means that a long url, such as 
[https://ultimaker.com/en/knowledge/33-reducing-costs-and-improving-efficiency-with-the-ultimaker-s5](https://ultimaker.com/en/knowledge/33-reducing-costs-and-improving-efficiency-with-the-ultimaker-s5) 
is expected to be shortened into an link, such as 
https://picoURL.com/y6q7ws9d 
where the string y6q7ws9d (short_code) is the hash key that is generated from the picoURL service.

In addition, the generated link has to be unique, meaning that two long links shall never point to the same short code.

### Prework

According to section 2.3 of [RFC 3986](https://www.ietf.org/rfc/rfc3986.txt), the characters that are allowed in a URI and are unreserved (have not specific purpose) are:
* The latin alphanumeric characters [0-9a-zA-Z] --> 62 characters
* The symbols "-" / "." / "_" / "~" --> 4 characters

The more characters we consider in the short codes, the greater the solution space.
For the sake of simplicity, we will use base64 encoding since there is already a [Python library for it](https://docs.python.org/2/library/base64.html). In our case, the base64 encoding will use alphanumeric characters and the symbols "-" and "_".  

*Note: In base64 each character has a length of 6 bits.* 

With 64 characters in our disposal, we can create the following number of links:

|len(short_code)| total short_codes  |
|-----|-----|
| 2 | 4096 |
| 3 | ~ 262k |
| 4 | ~ 16.7m |
| 5 | ~ 1bn |
| 6 | ~ 68.7bn |
| 7 | ~ 4.4tn |
| 8 | ~ 281.4tn |


TinyURL claims: 
> Making over a billion long URLs usable! Serving billions of redirects per month.

1bn of redirects per month translates to 1billion / (30 days * 24 hours * 3600 seconds) = ~385 redirects per second.

Let's say that we want to ensure the production of 1 billion URLs per year. Then we will have
1,000,000,000 / (12 months * 30 days * 24 hours * 3600 s) = ~32 URL shortenings per second. Let's round it to 30 POST requests per second. 
If we want our service to be available for at least 5 years, we will need to produce 5 billion short entries, therefore, according to the table above, we need to have at least 6 characters in our short code.


### Initial thoughts
The first instict would be to hash the long URL through a hashing function (e.g. MD5 or SHA1) and truncate the result to keep only the first 6-10 characters of the hash. Since we expect that collisions will arise (especially if many users request to shorten the same URL), we can use a collision strategy, such as: 
1. Iterating over the hash, with a window of 6-10 characters, until we find a hash that does not exist in the database.
2. Append a random number to the URL and rehash it. Repeat until a non-existing hash is produced.

or any other collision strategy.

Alternatively, instead of hashing the original link, we could pre-generate a database that contains all n-character words of a base64 encoding. In this case, we would just need to have enough storage for this database and whenever a new shortening request comes, we pop a random short code and assign it to the long link.

Let's see these two options in more detail.


### Option 1: Hashing and truncating

To generate the 6-character code, we will follow the example of git and use SHA-1 hasing method (160 bits). If we encode these 160bits in base64, it will result in 26 characters. From these characters we only need the first 6, or, alternatively, **the first 36 bits of the hash**.

After searching git's approachs to shorten the links, I encountered the [the birthday problem](https://en.wikipedia.org/wiki/Birthday_problem). 

According to that, for a 32-bit word, it takes only 77k hashed short codes to have been generated before our hashing function starts encountering a 50% chance of collisions and only 110k codes to encounter 75% of collisions. 

Our assumptions for 30 POST requests per second will lead to the generation of 110k codes in only 110000 / (30 requests * 3600 seconds) = ~1hour! So, after the first hour, our server will already start requiring at least 4 hash calculations to find a new hash.

Therefore, we see that, even though in principle a 6-character short code is enough, it will start become a problem very, very soon! 

**Note: Let's assume that 75% chance of collision is the maximum acceptable collision rate.**

For an 8-character short code:
* 8-character, base64 code = 48 bits word
* 75% chance of collisions: ~28m reserved short_codes --> ~ 10 days

For a 10-character short code:
* 10-character, base64 code = 60 bits word
* 75% chance of collisions ~5bn reserved short_codes --> ~ 5.35 years

In the case that our traffic increases even more, we can just lengthen the short code size from 10 to 11 or even 12, same as TinyURL does.

## Option 2: Using a database with pre-generated hashes

Using the `product` function from `itertools` module, we can get all possible n-letter strings. Since this is a generator, running the following function can give us an idea of how much time it could take to generate all the short codes.    
```python
	import time
	from itertools import product

	def short_code_generation(n):
	    base64 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-_'
	    c = 0

	    start = time.time()
	    for _ in product(base64, repeat=n):
	        c += 1
	    print("Short code size: {}".format(n))
	    print("Execution time: {}s".format(time.time() - start))
	    print("Solution space: {}".format(c))
```
Running the above function for n = 5 we can get all the combinations of the base64 characters in 5-character words, which means we can get ~1b values in 75seconds. This will result in a database of approximate size 1b words * 5 bytes/word = 5bn bytes or ~5GB of data.

For 6-character words it results in a database of approximate size 64 ^ 6 word  * 6bytes/word = 384GB of data. How long would it take to create this database is a mystery, as I tried running the above function for n = 6 and it hadn't finished after 5 hours.

One more thing to note in this scenario is that if the database goes out of service, the whole system collapses, in which case we will need a backup database. This will double the required hard drive memory from 384GB to 768GBs and will need a safe database synchronization mechanism.

## Making a decision

| Criteria | Hashed codes | Hash DB |
|---|---|---|
| Preconditions  | - | Hash DB has to be prefilled |
| Can suffer perfomance loss | Yes, when collision chance exceeds 75% | No
| Can be extended easily | Yes, just change the short code size | Yes, but filling the database and its replica with the new set of short codes can take time and will require more memory
| Optimal short code size | 10 | 6


On a more phylosophical note, does size really matter? Some people would argue that the bigger, the better! 

For an actual product, where the costs of the deployment would not be an issue, I would go for the second option and have a replica database of hash codes to avoid the single point of failure. This option provides shorter codes and avoid the possibility of latencies when requesting a new short url.

Nevertheless, for the weekend project, I will go with the first option, as I think that hashing is more fun than pre generating a database.

## Other things to consider

* How big do we expect the URL mapping database to grow?

In the main database we want to store:
* The original URL (URL does not have a size limitation according to [this source](https://stackoverflow.com/questions/417142/what-is-the-maximum-length-of-a-url-in-different-browsers), but a maximum size of 2000 bytes is prefered)
* The short code (10 characters. To be on the safe side, we will allocate 12 characters for future uses --> 12 bytes)
* The creation date (datetime object --> 8 bytes)
* The amount of times it has been used (big integer --> 8 bytes)

Considering that the short code must be unique, it can be used as the primary key.

Storing a total of 5billion entries means:
5 billion * 2028 bytes = ~ 10TB of data for 5 years.

The database table will be as follows:

| url | |
|---|---|
| short_code [pk] | varchar(12) |
| original_url | varchar(2000) |
| creation_date | timestamp |
| times_used | bigint |


Since we have only one table and there are no relations, we have the freedom to choose any SQL or NoSQL database. A NoSQL would fit the best, if we want to scale the application, but we will stick with SQL for simplicity and out of the box integration with Django.

In regards to the technologies, I will use Python 3 and Django to build the application.
