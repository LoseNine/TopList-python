from App import db

class Block(db.Model):
    __tablename__='block'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(128))
    hots=db.relationship('Hot',
                         backref='block',
                         cascade='all,delete-orphan')

    @classmethod
    def addBlock(cls,name):
        try:
            block=Block(name=name)
            db.session.add(block)
            db.session.commit()
            return 0
        except:
            print('rolllback')
            db.session.rollback()
            return 1

    @classmethod
    def getBlocks(cls):
        return Block.query.all()

class Hot(db.Model):
    __tablename__='hot'
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.Text())
    content=db.Column(db.Text(),nullable=True)
    url=db.Column(db.Text())
    block_id=db.Column(db.Integer,db.ForeignKey('block.id'))

    @classmethod
    def addHot(cls,block,title,content,url):
        try:
            b=Block.query.filter_by(name=block).first().id
            hot=Hot(title=title,content=content,url=url,block_id=b)
            db.session.add(hot)
            db.session.commit()
            return 0
        except:
            print('rolllback')
            db.session.rollback()
            return 1
