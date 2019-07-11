# coding: utf-8
from sqlalchemy import Column, Date, Index, String, text, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, LONGTEXT
from .extensions import db, ma

def add_schema(cls):
    class Schema(ma.ModelSchema):
        class Meta:
            model = cls
    cls.Schema = Schema
    return cls


@add_schema
class ActionCategory(db.Model):
    __tablename__ = 'action_category'
    __table_args__ = (
        Index('unique_action_category', 'action_id', 'category_id', unique=True),
    )

    id = Column(BIGINT(20), primary_key=True)
    action_id = Column(BIGINT(20), nullable=False)
    category_id = Column(INTEGER(11))


@add_schema
class Category(db.Model):
    __tablename__ = 'category'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(255))
    icon = Column(String(245))
    description = Column(String(4500))
    ordinal = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    parent_id = Column(INTEGER(11))
    status = Column(INTEGER(11))
    used_for_search = Column(INTEGER(11))
    used_for_filter = Column(INTEGER(11))


@add_schema
class ClientSetting(db.Model):
    __tablename__ = 'client_setting'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45), unique=True)
    version = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    value = Column(String(5000))


@add_schema
class CommentImage(db.Model):
    __tablename__ = 'comment_image'
    __table_args__ = (
        Index('idx_unique_comment_image', 'comment_id', 'image_id', unique=True),
    )

    id = Column(BIGINT(20), primary_key=True)
    comment_id = Column(BIGINT(20), nullable=False)
    image_id = Column(BIGINT(20), nullable=False)
    created_time = Column(BIGINT(20), nullable=False)


@add_schema
class Following(db.Model):
    __tablename__ = 'following'
    __table_args__ = (
        Index('idx_unique_following', 'user_id', 'following_user_id', unique=True),
    )

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    following_user_id = Column(BIGINT(20), nullable=False)
    inserted_time = Column(BIGINT(20))
    status = Column(INTEGER(11))
    updated_time = Column(BIGINT(20))


@add_schema
class Image(db.Model):
    __tablename__ = 'image'

    id = Column(BIGINT(20), primary_key=True)
    title = Column(String(45))
    description = Column(String(4500))
    image_link = Column(String(255), nullable=False)
    status = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    created_time = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
    user_id = Column(BIGINT(20), nullable=False, server_default=text("'0'"))


@add_schema
class KindnessAction(db.Model):
    __tablename__ = 'kindness_action'

    id = Column(BIGINT(20), primary_key=True)
    title = Column(String(1000))
    content = Column(LONGTEXT)
    status = Column(INTEGER(11))
    created_time = Column(BIGINT(20))


@add_schema
class KindnessActionImage(db.Model):
    __tablename__ = 'kindness_action_image'
    __table_args__ = (
        Index('idx_unique_image', 'kindness_action_id', 'image_id', unique=True),
    )

    id = Column(BIGINT(20), primary_key=True)
    kindness_action_id = Column(BIGINT(20), nullable=False)
    image_id = Column(BIGINT(20), nullable=False)
    created_time = Column(BIGINT(20))


@add_schema
class ServerSetting(db.Model):
    __tablename__ = 'server_setting'

    id = Column(INTEGER(11), primary_key=True)
    name = Column(String(45), unique=True)
    version = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    value = Column(String(5000))


@add_schema
class StoryAction(db.Model):
    __tablename__ = 'story_action'
    __table_args__ = (
        Index('idx_unique_story_action', 'story_id', 'action_id', unique=True),
    )

    id = Column(BIGINT(20), primary_key=True)
    story_id = Column(BIGINT(20), nullable=False)
    action_id = Column(BIGINT(20), nullable=False)
    created_time = Column(BIGINT(20))


@add_schema
class StoryComment(db.Model):
    __tablename__ = 'story_comment'

    id = Column(BIGINT(20), primary_key=True)
    story_id = Column(BIGINT(20), nullable=False)
    user_id = Column(BIGINT(20), nullable=False)
    content = Column(LONGTEXT)
    commented_time = Column(BIGINT(20))
    status = Column(INTEGER(11))


@add_schema
class StoryImage(db.Model):
    __tablename__ = 'story_image'
    __table_args__ = (
        Index('idx_unique_image', 'story_id', 'image_id', unique=True),
    )

    id = Column(BIGINT(20), primary_key=True)
    story_id = Column(BIGINT(20))
    image_id = Column(BIGINT(20), ForeignKey('image.id'))
    inserted_time = Column(BIGINT(20))


@add_schema
class StoryReaction(db.Model):
    __tablename__ = 'story_reaction'
    __table_args__ = (
        Index('idx_unique_user_story', 'story_id', 'user_id', unique=True),
    )

    id = Column(BIGINT(20), primary_key=True)
    story_id = Column(BIGINT(20), nullable=False)
    user_id = Column(BIGINT(20), nullable=False)
    reaction_id = Column(String(45), nullable=False)
    reaction_time = Column(BIGINT(20))
    status = Column(INTEGER(11), nullable=False, server_default=text("'0'"))


@add_schema
class SuggestKindnessAction(db.Model):
    __tablename__ = 'suggest_kindness_action'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    action_id = Column(BIGINT(20), nullable=False)
    inserted_time = Column(BIGINT(20), nullable=False)


@add_schema
class User(db.Model):
    __tablename__ = 'user'

    id = Column(BIGINT(20), primary_key=True)
    full_name = Column(String(64), nullable=False)
    email = Column(String(64), unique=True)
    phone = Column(String(32), unique=True)
    password = Column(String(128))
    gender = Column(INTEGER(11))
    avatar = Column(String(245))
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    push_token = Column(String(4500))
    device_id = Column(String(64))
    facebook_id = Column(String(64), unique=True)
    google_id = Column(String(64), unique=True)
    apple_id = Column(String(64), unique=True)
    birthday = Column(Date)
    is_confirm_follower = Column(INTEGER(11))


@add_schema
class UserDevice(db.Model):
    __tablename__ = 'user_device'
    __table_args__ = (
        Index('idx_unique_user_device', 'user_id', 'device_id', unique=True),
    )

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20))
    push_token = Column(String(4500))
    device_id = Column(String(64))
    inserted_time = Column(BIGINT(20))


@add_schema
class UserStory(db.Model):
    __tablename__ = 'user_story'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20), nullable=False)
    title = Column(String(450), nullable=False)
    content = Column(LONGTEXT, nullable=False)
    status = Column(INTEGER(11))
    created_time = Column(BIGINT(20))
    number_of_like = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    number_of_dislike = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    number_of_comment = Column(INTEGER(11), nullable=False, server_default=text("'0'"))


@add_schema
class KindnessFeed(db.Model):
    __tablename__ = 'kindness_feed'

    id = Column(BIGINT(20), primary_key=True)
    user_id = Column(BIGINT(20))
    source_user_id = Column(BIGINT(20))
    item_id = Column(BIGINT(20))
    item_type = Column(String(32))
    inserted_time = Column(BIGINT(20), nullable=False, server_default=text("'0'"))
