distributed-services
====================

This is a proof of concept implementation of a distributed, language independent system that exposes interfaces to user-provided services. A project for UBC cs311.

The idea is to be able to call services from different languages from a agnostic client over ZeroMQ sockets and recieve results. 

This is supposed to demonstrate that certain languages are more suited for certain purposes. For example, Scala is very useful for quick, functional development, while python is very good for more complicated calculations (by leveraging its module system and large bank of libraries).


**Dependencies**
