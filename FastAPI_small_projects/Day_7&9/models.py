# Build Database Schema

# Project "TASK MANAGEMENT SYSTEM"

# Entities
# User
# Project
# Task
# Comment

# SQL Alchemy Models

from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True)

    projects = relationship(
        "Project",
        back_populates="owner"
    )


# class Project(Base):
#
#     __tablename__ = "projects"
#
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     owner_id = Column(Integer, ForeignKey("users.id"))
#     owner = relationship("User", back_populates="projects")
#     tasks = relationship("Task", back_populates="project")
#
#
# class Task(Base):
#
#     __tablename__ = "tasks"
#
#     id = Column(Integer, primary_key=True)
#     title = Column(String)
#     project_id = Column(Integer, ForeignKey("projects.id"))
#     project = relationship("Project", back_populates="tasks")
#     comments = relationship("Comment", back_populates="task")
#
#
# class Comment(Base):
#
#     __tablename__ = "comments"
#
#     id = Column(Integer, primary_key=True)
#     content = Column(String)
#     task_id = Column(Integer, ForeignKey("tasks.id"))
#     user_id = Column(Integer, ForeignKey("users.id"))
#     task = relationship("Task", back_populates="comments")