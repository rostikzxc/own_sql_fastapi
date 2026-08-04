import time
import asyncio

async def request(name: str):
    print (f"{name}: куколд")
    time.sleep(2)
    print (f"{name}: поч")

async def main():

    now = time.perf_counter()

    await asyncio.gather(
        request("Игорь"),
        request("Ярослав"),
        request("Артемий")
    )
    
    print(f"Ебать долго аж: {time.perf_counter() - now:.3f}")

asyncio.run(main())