from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Callable, Set

class RuleType(Enum):
    TOTAL_COUNT = 'TOTAL_COUNT'
    ALL_HAVE_PROPERTIES = 'ALL_HAVE_PROPERTIES'
    ALL_VERIFY_COMPARISON = 'ALL_VERIFY_COMPARISON'


@dataclass
class Rule:
    type: RuleType

    input_list_builder: Callable[[List], List]
    
    operator: Callable[[List], bool]
    description: str
    value: Any


def parse_rules(rules_text) -> List[Rule]:
    rules = []
    for rule_str in rules_text.split(';'):
        rule_str = rule_str.strip()
        
        if rule_str.startswith(RuleType.TOTAL_COUNT.value):
            rule_type = RuleType.TOTAL_COUNT
            rule_input_list_builder = total_count_input_builder
            rule_body = rule_str[len(RuleType.TOTAL_COUNT.value):].strip()
            rule_operator, rule_value, rule_description = _comparison_parser(rule_body, 'Total count', rule_str)
            rules.append(Rule(type=rule_type, input_list_builder=rule_input_list_builder, operator=rule_operator, value=rule_value, description=rule_description))

        elif rule_str.startswith(RuleType.ALL_VERIFY_COMPARISON.value):
            rule_type = RuleType.ALL_VERIFY_COMPARISON
            rule_body = rule_str[len(RuleType.ALL_VERIFY_COMPARISON.value):].strip()
            if not (rule_body.startswith('[') and rule_body.endswith(']')):
                raise ValueError(f'Invalid rule: {rule_str}')
            rule_body = rule_body[1:-1].strip()
            property = rule_body.replace('>','=').replace('<', '=').split('=')[0].strip()
            rule_input_list_builder = lambda data, p=property: [item[p] for item in data]

            rule_body = rule_body[len(property):].strip()
            rule_operator, rule_value, rule_description = _comparison_parser(rule_body, property, rule_str)
            rules.append(Rule(type=rule_type, input_list_builder=rule_input_list_builder, operator=rule_operator, value=rule_value, description=rule_description))

        elif rule_str.startswith("ALL_HAVE_PROPERTIES"):
            rule_type = RuleType.ALL_HAVE_PROPERTIES
            rule_body = rule_str[len(RuleType.ALL_HAVE_PROPERTIES.value):].strip()
            if not (rule_body.startswith('[') and rule_body.endswith(']')):
                raise ValueError(f'Invalid rule: {rule_str}')
            rule_body = rule_body[1:-1].strip()

            rule_input_list_builder = lambda data: data

            fields = set([field.strip() for field in rule_body.split(',')])
            rule_operator = all_have_properties_operator
            rule_description = f'All items should have the following properties: {fields}'
            rules.append(Rule(type=rule_type, input_list_builder=rule_input_list_builder, operator=rule_operator, value=fields, description=rule_description))
        elif rule_str:
            raise ValueError(f'Invalid rule: {rule_str}')
    return rules
            

def _comparison_parser(rule_body, comparison_subject, entire_rule):
    '''
    Parse a comparison rule


    Parameters
    ----------
    rule_body : str
        The body of the rule, e.g. "= 10"
    comparison_subject : str
        what is being compared, e.g. "TOTAL_COUNT"
    entire_rule : str
        The entire rule, e.g. "TOTAL_COUNT>0"

    Returns
    -------
    rule_operator : Callable[[List], bool]
        The operator function to be used in the comparison
    rule_description : str
        A description of the rule
    '''
    if rule_body.startswith('='):
        rule_operator = equality_operator
        rule_value = rule_body[1:].strip()
        rule_value = int(rule_value) if rule_value.isdigit() else rule_value.replace('"', '')
        rule_description = f'{comparison_subject} should be equal to {rule_value}'
    elif rule_body.startswith('>'):
        rule_operator = greater_than_operator
        rule_value = rule_body[1:].strip()
        rule_value = int(rule_value) if rule_value.isdigit() else rule_value.replace('"', '')
        rule_description = f'{comparison_subject} should be greater than {rule_value}'
    elif rule_body.startswith('<'):
        rule_operator = less_than_operator
        rule_value = rule_body[1:].strip()
        rule_value = int(rule_value) if rule_value.isdigit() else rule_value.replace('"', '')
        rule_description = f'{comparison_subject} should be less than {rule_value}'
    else:
        raise ValueError(f'Invalid rule: {entire_rule}')
    return rule_operator, rule_value, rule_description
    

def total_count_input_builder(data: List) -> List:
    return [len(data)]


def equality_operator(input_list: List, value: Any) -> bool:
    for item in input_list:
        if item != value:
            return False
    return True


def greater_than_operator(input_list: List, value: int) -> bool:
    for item in input_list:
        if item is None or item <= value:
            return False
    return True


def less_than_operator(input_list: List, value: int) -> bool:
    for item in input_list:
        if item is None or item >= value:
            return False
    return True


def all_have_properties_operator(input_list: List, fields: Set) -> bool:
    for item in input_list:
        item_keys = set(item.keys())
        if not fields.issubset(item_keys):
            return False
        for field in fields:
            if item[field] is None or item[field] == '':
                return False
    return True
