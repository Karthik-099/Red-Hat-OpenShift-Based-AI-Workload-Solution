import requests
import time
import statistics
import concurrent.futures
import random

API_URL = "http://localhost:8000/predict"

def make_prediction():
    data = [random.uniform(-10, 10) for _ in range(10)]
    start_time = time.time()
    try:
        response = requests.post(API_URL, json={"data": data}, timeout=5)
        latency = (time.time() - start_time) * 1000
        return {
            "success": response.status_code == 200,
            "latency": latency,
            "status_code": response.status_code
        }
    except Exception as e:
        return {
            "success": False,
            "latency": 0,
            "error": str(e)
        }

def run_load_test(num_requests=1000, num_workers=10):
    print(f"Starting load test with {num_requests} requests using {num_workers} workers")
    
    results = []
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(make_prediction) for _ in range(num_requests)]
        for future in concurrent.futures.as_completed(futures):
            results.append(future.result())
    
    total_time = time.time() - start_time
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    latencies = [r["latency"] for r in successful]
    
    print("\n" + "="*50)
    print("Load Test Results")
    print("="*50)
    print(f"Total Requests: {num_requests}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print(f"Success Rate: {len(successful)/num_requests*100:.2f}%")
    print(f"Total Time: {total_time:.2f}s")
    print(f"Requests/sec: {num_requests/total_time:.2f}")
    
    if latencies:
        print(f"\nLatency Statistics:")
        print(f"  Min: {min(latencies):.2f}ms")
        print(f"  Max: {max(latencies):.2f}ms")
        print(f"  Mean: {statistics.mean(latencies):.2f}ms")
        print(f"  Median: {statistics.median(latencies):.2f}ms")
        print(f"  P95: {statistics.quantiles(latencies, n=20)[18]:.2f}ms")
        print(f"  P99: {statistics.quantiles(latencies, n=100)[98]:.2f}ms")
    
    print("="*50)

if __name__ == "__main__":
    run_load_test(num_requests=1000, num_workers=10)
