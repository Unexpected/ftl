from core.model import *

"""
def load_model():
    db_session = get_db_session()
    for module in db_session.query(Module).all():
        if module.name == "core":
            continue

        for entity in module.entities:
            table_name = entity.table_name
            if not table_name:
                table_name = entity.name
            attr_dict = {'__tablename__': table_name}
            if entity.schema_name != None:
                attr_dict['__table_args__'] = {'schema': entity.schema_name}

            pk_attributes = set()
            for key in entity.keys:
                if key.key_type == 0:
                    for key_attribute in key.key_attributes:
                        pk_attributes.add(key_attribute.attribute_name)

            for attribute in entity.attributes:
                data_type_class = None
                if attribute.data_type == 0:
                    data_type_class = Integer
                elif attribute.data_type == 1:
                    data_type_class = String(attribute.length)
                elif attribute.data_type == 2:
                    data_type_class = Date
                elif attribute.data_type == 3:
                    data_type_class = Boolean

                if attribute.name in pk_attributes:
                    column = Column(data_type_class, primary_key=True)
                else:
                    column = Column(data_type_class)

                attr_dict[attribute.name] = column

            Base = declarative_base()
            className = entity.name[0].upper() + entity.name[1:]
            MyClass = type(className, (Base,), attr_dict)
            print(MyClass)
"""


def get_core_metadata():
    """ Initial core metamodel definition 
    Unlike other entities, core model for Entities, Attributes, etc. is hardcoded, this fills tables with 
    self definition to allow prototyping """
    core_entities = []
    core_entities.append(Entity(name='entity', schema_name='core',
                                table_name='entity', label='Entity', comment='Entity model'))

    core_keys = []
    core_keys.append(Key(name='entity_pk', entity_name='entity',
                         label='Entity PK', comment='Entity primary key', key_type=0))

    core_attributes = []
    core_attributes.append(Attribute(name='name', entity_name='entity',
                                     data_type=1, length=80, mandatory=True, order=0, label='Name'))
    core_attributes.append(Attribute(name='database_name', entity_name='entity',
                                     data_type=1, length=80, mandatory=False, order=5, label='Database Name'))
    core_attributes.append(Attribute(name='schema_name', entity_name='entity',
                                     data_type=1, length=80, mandatory=False, order=10, label='Schema Name'))
    core_attributes.append(Attribute(name='table_name', entity_name='entity',
                                     data_type=1, length=80, mandatory=True, order=15, label='Table Name'))
    core_attributes.append(Attribute(name='label', entity_name='entity',
                                     data_type=1, length=250, mandatory=True, order=20, label='Label'))
    core_attributes.append(Attribute(name='comment', entity_name='entity',
                                     data_type=1, length=4000, mandatory=False, order=25, label='Comment'))

    core_key_attributes = []
    core_key_attributes.append(KeyAttribute(
        key_name='entity_pk', attribute_name='name', entity_name='entity', order=0))

    core_entities.append(Entity(name='attribute', schema_name='core',
                                table_name='attribute', label='Attribute', comment='Attribute model'))

    core_attributes.append(Attribute(name='name', entity_name='attribute',
                                     data_type=1, length=80, mandatory=True, order=0, label='Name'))
    core_attributes.append(Attribute(name='entity_name', entity_name='attribute',
                                     data_type=1, length=80, mandatory=True, order=5, label='Entity Name'))
    core_attributes.append(Attribute(name='data_type', entity_name='attribute',
                                     data_type=0, length=3, mandatory=True, order=10, label='Data type'))
    core_attributes.append(Attribute(name='length', entity_name='attribute',
                                     data_type=0, length=8, mandatory=True, order=15, label='Length'))
    core_attributes.append(Attribute(name='length_scale', entity_name='attribute',
                                     data_type=0, length=8, mandatory=True, order=20, label='Length scale'))
    core_attributes.append(Attribute(name='mandatory', entity_name='attribute',
                                     data_type=4, length=8, mandatory=True, order=25, label='Mandatory'))
    core_attributes.append(Attribute(name='order', entity_name='attribute',
                                     data_type=0, length=8, mandatory=True, order=30, label='Order'))
    core_attributes.append(Attribute(name='label', entity_name='attribute',
                                     data_type=1, length=250, mandatory=True, order=35, label='Label'))
    core_attributes.append(Attribute(name='caption', entity_name='attribute',
                                     data_type=1, length=250, mandatory=True, order=40, label='Caption'))
    core_attributes.append(Attribute(name='placeholder', entity_name='attribute',
                                     data_type=1, length=250, mandatory=True, order=45, label='Placeholder'))
    core_attributes.append(Attribute(name='tooltip', entity_name='attribute',
                                     data_type=1, length=250, mandatory=True, order=50, label='Tooltip'))
    core_attributes.append(Attribute(name='comment', entity_name='attribute',
                                     data_type=1, length=4000, mandatory=True, order=55, label='Comment'))
    core_attributes.append(Attribute(name='initial_value', entity_name='attribute',
                                     data_type=1, length=250, mandatory=True, order=60, label='Initial Value'))
    core_attributes.append(Attribute(name='default_value', entity_name='attribute',
                                     data_type=1, length=250, mandatory=True, order=65, label='Default Value'))

    core_keys.append(Key(name='attribute_pk', entity_name='attribute',
                         label='Attribute PK', comment='Attribute primary key', key_type=0))

    core_key_attributes.append(KeyAttribute(
        key_name='attribute_pk', attribute_name='name', entity_name='attribute', order=0))
    core_key_attributes.append(KeyAttribute(
        key_name='attribute_pk', attribute_name='entity_name', entity_name='attribute', order=0))

    # Key
    core_entities.append(Entity(name='key', schema_name='core',
                                table_name='key', label='Key', comment='Key model'))

    core_attributes.append(Attribute(name='name', entity_name='key',
                                     data_type=1, length=80, mandatory=True, order=0, label='Name'))
    core_attributes.append(Attribute(name='entity_name', entity_name='key',
                                     data_type=1, length=80, mandatory=True, order=5, label='Entity name'))
    core_attributes.append(Attribute(name='label', entity_name='key',
                                     data_type=1, length=250, mandatory=True, order=10, label='Label'))
    core_attributes.append(Attribute(name='comment', entity_name='key',
                                     data_type=1, length=4000, mandatory=False, order=15, label='Comment'))
    core_attributes.append(Attribute(name='key_type', entity_name='key',
                                     data_type=0, length=10, mandatory=True, order=20, label='Key type'))
    core_attributes.append(Attribute(name='target_key', entity_name='key',
                                     data_type=1, length=80, mandatory=False, order=25, label='Target key name'))
    core_attributes.append(Attribute(name='target_entity', entity_name='key',
                                     data_type=1, length=80, mandatory=False, order=30, label='Target entity name'))

    target_key = Column(String(80))
    target_entity = Column(String(80))

    core_keys.append(Key(name='key_pk', entity_name='key',
                         label='Key PK', comment='Key primary key', key_type=0))

    core_key_attributes.append(KeyAttribute(
        key_name='key_pk', attribute_name='name', entity_name='key', order=0))
    core_key_attributes.append(KeyAttribute(
        key_name='key_pk', attribute_name='entity_name', entity_name='key', order=5))

    # KeyAttribute
    core_entities.append(Entity(name='key_attribute', schema_name='core',
                                table_name='key_attribute', label='Key attribute', comment='Key attribute model'))

    core_attributes.append(Attribute(name='key_name', entity_name='key_attribute',
                                     data_type=1, length=80, mandatory=True, order=0, label='Key name'))
    core_attributes.append(Attribute(name='attribute_name', entity_name='key_attribute',
                                     data_type=1, length=80, mandatory=True, order=5, label='Attribute name'))
    core_attributes.append(Attribute(name='entity_name', entity_name='key_attribute',
                                     data_type=1, length=80, mandatory=True, order=10, label='Entity name'))
    core_attributes.append(Attribute(name='order', entity_name='key_attribute',
                                     data_type=0, length=10, mandatory=True, order=15, label='Order'))

    core_keys.append(Key(name='key_attribute_pk', entity_name='key_attribute',
                         label='Key attribute PK', comment='Key attribute primary key', key_type=0))

    core_key_attributes.append(KeyAttribute(
        key_name='key_attribute_pk', attribute_name='key_name', entity_name='key_attribute', order=0))
    core_key_attributes.append(KeyAttribute(
        key_name='key_attribute_pk', attribute_name='attribute_name', entity_name='key_attribute', order=5))
    core_key_attributes.append(KeyAttribute(
        key_name='key_attribute_pk', attribute_name='entity_name', entity_name='key_attribute', order=10))

    # Module
    core_entities.append(Entity(name='module', schema_name='core',
                                table_name='module', label='Module', comment='Module model'))

    core_attributes.append(Attribute(name='name', entity_name='module',
                                     data_type=1, length=80, mandatory=True, order=0, label='Module name'))
    core_attributes.append(Attribute(name='label', entity_name='module',
                                     data_type=1, length=250, mandatory=True, order=5, label='Label'))
    core_attributes.append(Attribute(name='comment', entity_name='module',
                                     data_type=1, length=4000, mandatory=True, order=10, label='Comment'))

    core_keys.append(Key(name='module_pk', entity_name='module',
                         label='Module PK', comment='Module primary key', key_type=0))

    core_key_attributes.append(KeyAttribute(
        key_name='module_pk', attribute_name='name', entity_name='module', order=0))

    core_module = Module(name='core', label='FTL',
                         comment='FTL Prototyper module')
    core_module.entities = core_entities

    return core_entities, core_attributes, core_keys, core_key_attributes, core_module
