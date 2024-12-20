import json
import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, load_dora_inputs_and_task, create_agent_output

import time
import pandas as pd
import numpy as np


class Operator:
    def __init__(self):
        self.final_num = 0
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            self.final_num +=1
            if self.final_num >=5:
                send_output("final_output", pa.array([create_agent_output(step_name='agent_response', output_data='完成',dataflow_status=os.getenv('IS_DATAFLOW_END',True))]),dora_event['metadata'])
                self.final_num = 0
        return DoraStatus.CONTINUE