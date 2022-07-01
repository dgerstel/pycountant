"""Help manage the cash flow every month.

Given that your company got
- a purchase order (PO)
- reimbursement of costs

find out how much should you pay:
- VAT
- salary to yourself
"""
from dataclasses import dataclass
from enum import Enum, auto


VAT = 20_00
TAX = 25_00

class Subjects(Enum):
    MYSELF = auto()
    CLIENT1 = auto()
    CLIENT2 = auto()


class Status(Enum):
    STARTED = auto()
    PAID = auto()
    ACCOUNTED_FOR = auto()


@dataclass
class PO:
    amount: int
    _from: Subjects
    vat: int
    tax: int
    fees: int
    fees_vat: int
    descr: str = ""
    status: Status = Status.STARTED


@dataclass
class Transfer:
    po: PO
    amount: int
    _from: Subjects
    _to: Subjects = Subjects.MYSELF
    descr: str = ""


def main():
    po1 = PO(amount=600_00, _from=Subjects.CLIENT1, vat=VAT, tax=TAX, fees=0, fees_vat=0, descr="Help with database")
    tr = Transfer(po=po1, amount=600_00, _from=Subjects.CLIENT1)
    print(tr)


if __name__ == "__main__":
    main()




