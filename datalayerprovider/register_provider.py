# MIT License
#
# Copyright (c) 2020, Bosch Rexroth AG
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os 
import sys
import signal
import time

import datalayer

import datalayerprovider.my_provider_node

connectionProvider = "tcp://boschrexroth:boschrexroth@127.0.0.1:2070"

def run_provider(provider : datalayer.provider.Provider):

    print("Starting provider...")
    provider_node = datalayerprovider.my_provider_node.MyProviderNode()
    with datalayer.provider_node.ProviderNode(provider_node.cbs, 1234) as node:
        result = provider.register_node("myData/myString", node)
        if result != datalayer.variant.Result.OK:
            print("Register Data Provider failed with: ", result)

        result= provider.start()
        if result != datalayer.variant.Result.OK:
            print("Starting Provider failed with: ", result)
            
        print("Provider started...")
        print("Running endless loop...")

        count=0
        while True:
            count=count+1
            if count > 9:
                break
            time.sleep(1)
        
        result = provider.stop()
        if result != datalayer.variant.Result.OK:
            print("Stopping Provider failed with: ", result)
        result = provider.unregister_node("myData/myString")
        if result != datalayer.variant.Result.OK:
            print("Unregister Data Provider failed with: ", result)

def run():
    print("Simple Snap for ctrlX Datalayer Provider with Python")
    print("Connect to ctrlX CORE: ", connectionProvider)

    print("Create and start ctrlX Datalayer System")
    with datalayer.system.System("") as datalayer_system:
        datalayer_system.start(False)

        print("Creating provider...")
        with datalayer_system.factory().create_provider(connectionProvider) as provider:

            run_provider(provider)

        datalayer_system.stop(True)







        