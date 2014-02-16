#!/usr/bin/python

class DC(Base):
    __table__ = Table("dc", Base.metadata,
                            autoload=True, autoload_with=some_engine)

