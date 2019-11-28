
from django.db import migrations


default_xsd = '''\
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema" elementFormDefault="qualified" attributeFormDefault="unqualified">
<xs:element name="Body">
<xs:complexType>
<xs:sequence>
<xs:element name="Entity">
<xs:complexType>
<xs:sequence>
    <xs:element name="Name" type="xs:string"></xs:element>
    <xs:element name="Phone">
        <xs:simpleType>
            <xs:restriction base="xs:string">
                <xs:pattern value="\+?\d{11,15}(;\+?\d{11,15})*;?"/>
            </xs:restriction>
        </xs:simpleType>
    </xs:element>
    <xs:element name="Email">  <!-- removed `type="xs:string"` -->
        <xs:simpleType>
            <xs:restriction base="xs:string">
                <xs:pattern value="[\w\d.\-_]+@[\w\d.\-_]+\.\w{2,24}(;[\w\d.\-_]+@[\w\d.\-_]+\.\w{2,24})*;?"/>
            </xs:restriction>
        </xs:simpleType>
    </xs:element>
    <xs:element name="Services">
        <xs:complexType>
        <xs:sequence>
            <xs:element name="Service" maxOccurs="unbounded">
                <xs:complexType>
                <xs:sequence>
                    <xs:element name="Name" type="xs:string"></xs:element>
                    <xs:element name="Availability">
                        <xs:complexType>
                        <xs:sequence>
                            <xs:element name="From" type="xs:string"></xs:element>
                            <xs:element name="To" type="xs:string"></xs:element>
                        </xs:sequence>
                        </xs:complexType>
                    </xs:element>
                </xs:sequence>
                <xs:attribute name="is_main" type="xs:boolean" use="required"></xs:attribute>
                </xs:complexType>
            </xs:element>
        </xs:sequence>
        </xs:complexType>
    </xs:element>
</xs:sequence>
</xs:complexType>
</xs:element>
</xs:sequence>
</xs:complexType>
</xs:element>
</xs:schema>
'''


def add_default_xsd(apps, _):
    Xsd = apps.get_model('info', 'Xsd')
    Xsd.objects.create(rule=default_xsd)


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_xsd'),
    ]

    operations = [
        migrations.RunPython(add_default_xsd),
    ]
