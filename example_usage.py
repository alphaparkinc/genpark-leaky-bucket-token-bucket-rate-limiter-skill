from client import TokenBucketLimiter, LeakyBucketLimiter

def main():
    tb = TokenBucketLimiter(capacity=5, refill_rate=2)
    print("Token Bucket consume 3:", tb.consume(3))
    print("Token Bucket consume 2:", tb.consume(2))
    print("Token Bucket consume 1 (should fail):", tb.consume(1))

    lb = LeakyBucketLimiter(capacity=5, leak_rate=2)
    print("Leaky Bucket add 4:", lb.add(4))
    print("Leaky Bucket add 2 (should fail):", lb.add(2))

if __name__ == "__main__":
    main()
