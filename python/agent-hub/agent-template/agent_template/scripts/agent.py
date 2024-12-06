import os
from dora import Node, DoraStatus
import pyarrow as pa
from mofa.kernel.utils.util import load_agent_config, create_agent_output, load_node_result
from mofa.run.run_agent import run_dspy_or_crewai_agent
from mofa.utils.files.dir import get_relative_path
from mofa.utils.log.agent import record_agent_result_log
class Operator:
    def __init__(self):
        self.task = None
    def on_event(
        self,
        dora_event,
        send_output,
    ) -> DoraStatus:
        if dora_event["type"] == "INPUT":
            if dora_event['id'] == "task": self.task =  dora_event["value"][0].as_py() # 如果是从terminal-input中，则直接使用这个方法，如果不是，使用下面的这个方法load_node_result(dora_event["value"][0].as_py())
            # if dora_event['id'] == "context_memory": self.context_memory =  load_node_result(dora_event["value"][0].as_py())
            if self.task is not None : # 判断task是否为空
                
                yaml_file_path = get_relative_path(current_file=__file__, sibling_directory_name='configs', target_file_name='agent.yml') # 默认不变，只修改target_file_name参数的文件名
                inputs = load_agent_config(yaml_file_path) # 读取yaml
                inputs["task"] = self.task # 给task赋值
                # if len(self.context_memory)>0:
                #     inputs['input_fields'] = {"memory_data":self.context_memory} # 如果这个node需要多个数据源，则使用这种方法. inputs['input_fields']可以接受一个dict,这个里面的内容就是说，我的agent需要接受的参数
                agent_result = run_dspy_or_crewai_agent(agent_config=inputs) # 自定义的agent,如果不需要agent,则需要自己根据需求创建流程
            
                record_agent_result_log(agent_config=inputs,agent_result={"2, "+ inputs.get('log_step_name', "Step_one"): agent_result}) # 将本地的agent结果记录下来
                send_output("agent_response", pa.array([create_agent_output(step_name='agent_response', output_data=agent_result,dataflow_status=os.getenv('IS_DATAFLOW_END',False))]),dora_event['metadata']) # 将agent结果发送到下一个node，dataflow_status如果是true则代表这个node结束了，整个流程就结束了，否则这个node只是一个流程中的一个步骤


                print('agent_response:',agent_result)
                self.task = None
        return DoraStatus.CONTINUE