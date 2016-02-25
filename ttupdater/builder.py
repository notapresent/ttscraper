"""Factory functions for creating application object graph"""
from webclient import WebClient
from parsers import Parser
from taskmaster import TaskMaster
from scraper import Scraper


def make_scraper():
    return Scraper(WebClient(), Parser())


def make_taskmaster():
    return TaskMaster()
