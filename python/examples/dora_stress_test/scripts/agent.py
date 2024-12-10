import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output

import time
import pandas as pd
import numpy as np


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

                # 测试6: Pandas DataFrame
                # 创建一个包含100万行和10列的DataFrame，列名为col0到col9。DataFrame中的每个元素都是一个0到1之间的随机数

                start_time = time.time()
                df = pd.DataFrame(np.random.rand(1000000, 10), columns=[f'col{i}' for i in range(10)])
                end_time = time.time()
                print(f"Creating DataFrame execution time: {end_time - start_time:.6f} seconds")
                # 记录创建DataFrame之后的时间，并计算创建DataFrame所需的时间：
                start_time = time.time()
                df['col_sum'] = df.sum(axis=1)
                end_time = time.time()
                #在DataFrame中添加一个新列col_sum，该列是其他10列的和（按行计算）
                print(f"Column-wise sum execution time: {end_time - start_time:.6f} seconds")

                # memory_usage = df.memory_usage(deep=True)  # deep=True 会递归计算对象的内存使用情况
                # print(memory_usage)
                # total_memory_usage = memory_usage.sum()
                # print(f"Total DataFrame memory usage: {total_memory_usage} bytes")
                # total_memory_usage_mb = total_memory_usage / 1024 ** 2  # 转换为MB
                # print(f"Total DataFrame memory usage: {total_memory_usage_mb:.2f} MB")
                send_output("agent_response", pa.array([create_agent_output(step_name='agent_response', output_data='完成',dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata'])

        return DoraStatus.CONTINUE