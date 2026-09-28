import json
import sys
from client import TokenBucketLimiter

limiters = {}

def handle_request(req):
    method = req.get("method")
    params = req.get("params", {})
    req_id = req.get("id")

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "check_rate_limit",
                        "description": "Check and consume rate limit tokens for a client key",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "client_id": {"type": "string"},
                                "capacity": {"type": "number", "default": 10},
                                "refill_rate": {"type": "number", "default": 5},
                                "amount": {"type": "number", "default": 1}
                            },
                            "required": ["client_id"]
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "check_rate_limit":
            cid = args["client_id"]
            if cid not in limiters:
                limiters[cid] = TokenBucketLimiter(args.get("capacity", 10), args.get("refill_rate", 5))
            allowed = limiters[cid].consume(args.get("amount", 1))
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps({"allowed": allowed, "client_id": cid})}]}
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
