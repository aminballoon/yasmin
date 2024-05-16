from std_msgs.msg import String
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup
from typing import List, Callable, Type, Any
from std_srvs.srv import Trigger
 
from yasmin import State
from yasmin import Blackboard
from simple_node import Node
from .basic_outcomes import ABORT, SUCCEED, WAITING

class BasicState(State):
    def __init__ (
        self,
        outcomes: List[str],
        execute_handler: Callable = None,
    ) -> None:
        _outcomes = [ABORT, SUCCEED, WAITING]

        if not outcomes is None:
            _outcomes = list(set(_outcomes + outcomes))
        super().__init__(_outcomes)
        self.__execute_handler = execute_handler


    def _is_canceled(self):
        if self.is_canceled():
            self._canceled = False
            return True
        return False
    
    def execute(self, blackboard: Blackboard) -> str:
        while True:
            if self.__execute_handler:
                outcome = self.__execute_handler(blackboard)
            print(self._canceled)
            if self._is_canceled():
                return ABORT
            if outcome != WAITING: break
        return outcome