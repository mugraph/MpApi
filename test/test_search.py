"""
Test the Search module
"""
from lxml import etree
from mpapi.search import Search
import pytest


one = """
<application xmlns="http://www.zetcom.com/ria/ws/module/search" 
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
             xsi:schemaLocation="http://www.zetcom.com/ria/ws/module/search http://www.zetcom.com/ria/ws/module/search/search_1_1.xsd">
    <modules>
        <module name="Object">
            <search limit="-1" offset="0">
                <expert>
                    <and>
                        <equalsField fieldPath="ObjCurrentLocationVoc" operand="4220560"/>
                        <notEqualsField fieldPath="__orgUnit" operand="EMPrimarverpackungen"/>
                        <notEqualsField fieldPath="__orgUnit" operand="AKuPrimarverpackungen"/>
                    </and>
                </expert>
            </search>
        </module>
    </modules>
</application>
"""

two = """
<application xmlns="http://www.zetcom.com/ria/ws/module/search" 
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
             xsi:schemaLocation="http://www.zetcom.com/ria/ws/module/search http://www.zetcom.com/ria/ws/module/search/search_1_1.xsd">
    <modules>
        <module name="Object">
            <search limit="-1" offset="0">
                <expert>
                    <and>
                        <equalsField fieldPath="ObjCurrentLocationVoc" operand="4220560"/>
                        <notEqualsField fieldPath="__orgUnit" operand="EMPrimarverpackungen"/>
                        <notEqualsField fieldPath="__orgUnit" operand="AKuPrimarverpackungen"/>
                        <not>
                            <contains fieldPath="ObjTextOnlineGrp.TextHTMLClb" operand="SM8HF"/>
                        </not>
                    </and>
                </expert>
            </search>
        </module>
    </modules>
</application>
"""


def test_one():
    # print(one)
    s = Search(fromString=one)
    assert s.validate(mode="search") is True


def test_two():
    s = Search(fromString=two)
    assert s.validate(mode="search") is True


def test_three():
    s = Search(module="Object")
    s.addCriterion(
        operator="equalsField",
        field="ObjCurrentLocationVoc",
        value="4220560",  # O1.189.01.K1 M13
    )
    assert s.validate(mode="search") is True


def test_four():
    s = Search(module="Object")
    s.AND()
    s.addCriterion(
        operator="equalsField",
        field="ObjCurrentLocationVoc",
        value="4220560",  # O1.189.01.K1 M13
    )
    s.addCriterion(
        operator="notEqualsField",  # notEqualsTerm
        field="ObjPublicationGrp.TypeVoc",
        value="2600647",  # use id? Daten freigegeben für SMB-digital
    )
    s.addCriterion(
        operator="notEqualsField",  # notEqualsTerm
        field="__orgUnit",  # __orgUnit is not allowed in Zetcom's own search.xsd
        value="EMPrimarverpackungen",  # 1632806EM-Primärverpackungen
    )

    assert s.validate(mode="search") is True


def test_five():
    s = Search(module="Object")
    s.addCriterion(
        operator="equalsField",
        field="ObjCurrentLocationVoc",
        value="4220560",  # O1.189.01.K1 M13
    )
    s.AND()
    s.addCriterion(
        operator="notEqualsField",  # notEqualsTerm
        field="ObjPublicationGrp.TypeVoc",
        value="2600647",  # use id? Daten freigegeben für SMB-digital
    )
    s.addCriterion(
        operator="notEqualsField",  # notEqualsTerm
        field="__orgUnit",  # __orgUnit is not allowed in Zetcom's own search.xsd
        value="EMPrimarverpackungen",  # 1632806EM-Primärverpackungen
    )

    with pytest.raises(Exception) as e_info:
        s.validate(mode="search")


def test_six():
    s = Search(module="Object")
    s.AND()
    s.addCriterion(
        operator="equalsField",
        field="ObjCurrentLocationVoc",
        value="4220560",  # O1.189.01.K1 M13
    )
    s.addCriterion(
        operator="notEqualsField",  # notEqualsTerm
        field="ObjPublicationGrp.TypeVoc",
        value="2600647",  # use id? Daten freigegeben für SMB-digital
    )
    s.addCriterion(
        operator="notEqualsField",  # notEqualsTerm
        field="__orgUnit",  # __orgUnit is not allowed in Zetcom's own search.xsd
        value="EMPrimarverpackungen",  # 1632806EM-Primärverpackungen
    )
    s.NOT()
    s.addCriterion(
        operator="contains",
        field="ObjTextOnlineGrp.TextHTMLClb",
        value="SM8HF",
    )
    # s.print()
    s.toFile(path="search.tmp.xml")
    assert s.validate(mode="search") is True


def test_seven():  # addField
    s = Search(module="Object")
    s.AND()
    s.addCriterion(
        operator="equalsField",
        field="ObjCurrentLocationVoc",
        value="4220560",  # O1.189.01.K1 M13
    )
    s.addCriterion(
        operator="notEqualsField",  # notEqualsTerm
        field="ObjPublicationGrp.TypeVoc",
        value="2600647",  # use id? Daten freigegeben für SMB-digital
    )
    s.addCriterion(
        operator="notEqualsField",  # notEqualsTerm
        field="__orgUnit",  # __orgUnit is not allowed in Zetcom's own search.xsd
        value="EMPrimarverpackungen",  # 1632806EM-Primärverpackungen
    )
    s.NOT()
    s.addCriterion(
        operator="contains",
        field="ObjTextOnlineGrp.TextHTMLClb",
        value="SM8HF",
    )
    s.addField(field="__id")
    # s.print()
    s.toFile(path="search.tmp.xml")
    assert s.validate(mode="search") is True


def test_attributes():
    q = Search(module="Object")
    q.AND()
    q.addCriterion(
        operator="equalsField",
        field="ObjCurrentLocationVoc",
        value="4220560",  # O1.189.01.K1 M13
    )
    q.addCriterion(
        operator="notEqualsField",  # notEqualsTerm
        field="ObjPublicationGrp.TypeVoc",
        value="2600647",  # use id? Daten freigegeben für SMB-digital
    )
    assert q.offset() == 0
    q.offset(value="123")
    assert q.offset(value="123")
    assert q.limit() == -1
    q.limit(value=10)
    assert q.limit() == 10
