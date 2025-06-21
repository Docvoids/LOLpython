from dataclasses import dataclass
from typing import Any, List, Optional

@dataclass
class ASTNode: pass
@dataclass
class ExpressionNode(ASTNode): pass
@dataclass
class LiteralNode(ExpressionNode): value: Any
@dataclass
class IdentifierNode(ExpressionNode): name: str
@dataclass
class BinaryOpNode(ExpressionNode): left: ExpressionNode; op: str; right: ExpressionNode
@dataclass
class FuncCallNode(ExpressionNode):
    callee: ExpressionNode
    args: List[ExpressionNode]
@dataclass
class StatementNode(ASTNode): pass
@dataclass
class ProgramNode(ASTNode): statements: List[StatementNode]
@dataclass
class VarDeclNode(StatementNode): name: str; initializer: Optional[ExpressionNode]
@dataclass
class AssignmentNode(StatementNode): target: ExpressionNode; expression: ExpressionNode
@dataclass
class VisibleNode(StatementNode): expressions: List[ExpressionNode]
@dataclass
class FuncDefNode(StatementNode): name: str; params: List[IdentifierNode]; body: List[StatementNode]
@dataclass
class ReturnNode(StatementNode):
    value: Optional[ExpressionNode]
@dataclass
class IfNode(StatementNode):
    condition: ExpressionNode
    if_block: List[StatementNode]
    else_block: Optional[List[StatementNode]]
    
