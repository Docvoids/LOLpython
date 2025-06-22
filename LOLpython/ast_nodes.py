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
class FuncCallNode(ExpressionNode): callee: ExpressionNode; args: List[ExpressionNode]
@dataclass
class NewInstanceNode(ExpressionNode): class_name: IdentifierNode
@dataclass
class MemberAccessNode(ExpressionNode): object: ExpressionNode; member: IdentifierNode
@dataclass
class MeNode(ExpressionNode): pass
@dataclass
class BukkitNode(ExpressionNode): pass
@dataclass
class BukkitAccessNode(ExpressionNode):
    bukkit: ExpressionNode
    index: ExpressionNode
@dataclass
class MaekNode(ExpressionNode):
    target: ExpressionNode
    target_type: str
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
class ReturnNode(StatementNode): value: Optional[ExpressionNode]
@dataclass
class IfNode(StatementNode):
    condition: ExpressionNode
    if_block: List[StatementNode]
    else_block: Optional[List[StatementNode]]
@dataclass
class ClassDefNode(StatementNode):
    name: str
    methods: List[FuncDefNode]
    properties: List[VarDeclNode]
