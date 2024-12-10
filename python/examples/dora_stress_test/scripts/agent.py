import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output

import time
import pandas as pd
import numpy as np
import time
import sys
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
class Operator:
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            agent_inputs = ['data','task']
            if dora_event["id"] in agent_inputs:
                task = dora_event["value"][0].as_py()

                sys.setrecursionlimit(3000)
                n = 35  # 注意：较大的n会显著增加计算时间
                start_time = time.time()
                fib_result = fibonacci(n)
                end_time = time.time()
                print(f"Fibonacci({n}) = {fib_result}")
                print(f"Fibonacci Execution time: {end_time - start_time:.6f} seconds")

                send_output("agent_response", pa.array([create_agent_output(step_name='agent_response', output_data='完成',dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])

        return DoraStatus.CONTINUE