.. Test Execution Hub documentation master file, created by
   sphinx-quickstart on Wed Mar 13 20:25:51 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. |br| raw:: html

   <br />

Backend
=======

This application provides the backend REST service for the `PUF
Frontend <https://github.com/FlorianFrank/puf_frontend>`__. It stores
the state of the GUI, connects to the Postgres databases storing CNT PUF
and memory PUF measurements. It additionally contains background runners
for evaluation and visualization tasks. It additionally provides
authentication functionality, a NATS client to delegate tests to
specific devices and direct access to the `Generic Test
Framework <https://github.com/FlorianFrank/generic_test_framework>`__.

Database Structure
------------------

Test123

Endpoints
---------

The app is written in python using Django as main backend framework.
Django allows us to subdivide the application into multiple apps with
different functionality:

-  .. rubric:: Authentication
      :name: authentication

   Provides the functionality required for the logging functionality,
   which is based on a token, which is passed from the frontend.

   -  It provides the following endpoints:

      -  **POST /authentication/logout** deletes the requested token and
         prevents access to all services after sending logout.

         -  **Parameters:**

            -  token: token to delete

         -  **Returns:** HTTP_205_RESET_CONTENT

-  .. rubric:: Dashboard Manager
      :name: dashboard-manager

   Provides all endpoints for widgets on the GUI dashboard

   -  It provides the following endpoints:

      -  **GET /dashboard/get_log_messages/** returns log messages from
         the backend

         -  **Parameters:**

            -  log_category: e.g. all or specific parts of the backend,
               e.g. evaluation_manager.
            -  log_type: e.g. Returns messages of a specific log type
            -  message_count: number of messages to retrieve.

         -  **Returns:**

            .. code-block:: json

               {"logMessages": [
                       "10:01:12 [Evaluation Manager] devices_view.py:34 ERROR: Receive request failed",
                       "10:01:12 [Evaluation Manager] devices_view.py:34 INFO: Receive request succeeded"]}

      -  **GET /dashboard/get_server_info/**

         -  **Returns:**

         .. code-block:: json

            {"serverinfo": [{"property": "IP", "value": "127.0.0.1"}, 
                           {"property": "Port", "value": 8000},       
                           {"property": "OS", "value": "UBUNTU LTS"}, 
                           {"property": "Online", "value": "31.12.2023 00:00"}]}

      -  **GET /dashboard/get_server_info/**

         -  **GET /dashboard/get_log_messages/** Returns memory
            consumption, cpu load and network traffic parameters from
            the backend

            -  **Returns:**

            .. code-block:: json
               
               {"current_memory_consumption": 10, "current_cpu_load": 4, "current_network_usage": 40, 
               "list_memory_consumption": [2.4, 2.8, 2.4], "list_cpu_load": [5.3,5.2, 8.5], "list_network_usage": [5.3,5.2, 8.5] }

-  .. rubric:: Device Manager
      :name: device-manager

   Provides all endpoints related to the device manager, e.g. to
   identify devices or to retrieve the wafer configuration.

   -  It provides the following endpoints:

      -  **GET /devices/get_devices/** returns all devices currently
         available in the databased, which is flushed after each
         startup.

         -  **Returns:**

         .. code-block:: json

              [{"name": "NANOSEC MicroService", "idn": "", "type": "nanosec_container", "protocol": "tcp_ip",
                "port": "10.42.0.180", "status": "online", "id": 0}] 

      -  **POST /device/add_device** manually adds a device to the
         backend. Other services are automatically added by an automatic
         discovery of the nats service

         -  **Parameters:** Device specific configuration

         -  **Returns:**:

            .. code-block:: json

               {"status": "ok"}
               {"status": "error"}

      -  **GET /device/get_wafer_configs** returns the available wafer
         configurations.

         -  **Parameters:** Device specific configuration

         -  **Returns:**:

            .. code-block:: json

               [{"waferID": 2, "pufID": 23, "row": 4, "column": 4, "rowsOnPUF": [1,2,3], "columnsOnPUF": [4,3,2]}]

      -  .. rubric:: Evaluation Manager
            :name: evaluation-manager

         Provides all endpoints to run evaluations, to list the
         available evaluation and visualization results and the
         endpoints to show evaluations and visualizations.

         -  It provides the following endpoints:

            -  **GET /evaluation/get_evaluation_types** returns the
               different evaluation and visualization methods, based on
               the selected test category.

               -  **Parameters:**

                  -  testCategory: Currently the test categories
                     “cnt_puf” and “memory” are supported.

               -  **Returns:**:

                  .. code-block:: json

                     {"evaluationMethods": [{"label": "Visualization of Raw data", "value": "rawFigure"},
                                              {"label": "Quantization (2-States)", "value": "quantize_2_states"},
                                              {"label": "Quantization (3-States)", "value": "quantize_3_states"},
                                              {"label": "Wafer Visualizer", "value": "waferVisualizer"}]

            -  **GET /evaluation/get_evaluation_types** returns the
               default configuration parameters of an evaluation or
               visualization method, identified by testType.

               -  **Parameters:**

                  -  testType: Currently the test categories “cnt_puf”
                     and “memory” are supported.

               -  **Returns:**
               
                  .. code-block:: json

                     {"label": "Raw Figure", "value": "rawFigure", 
                     "properties": [{"type": "select", "label": "scale", "name": "Scale", "values": ["linear", "log", "symlog"],
                     "default": "linear"}, { "type": "select", "label": "hide_legend", "name": "Hide Legend", "values": ["true", "false"],
                     "default": "false"}, "....."]}

            -  **GET /evaluation/get_connected_measurements** returns
               all measurements connected to a certain evaluation
               object.

               -  **Parameters:**

                  -  taskID: The evaluation task which is connected to
                     certain measurements.

               -  **Returns:**

               .. code-block:: json

                    {"measurements": ["id": 0, "testType": "TransferCharacteristic", "testTitle": "Test1",
                    "wafer": 2, "row": 7, "column": 8, "pufID": 23, "rowOnPUF": 4, "columnOnPUF": 3, "temperature": 23,
                    "iterations": 5, "selectedIteration": 3]}

            -  **GET /evaluation/start_evaluation** Schedules an
               evaluation in the evaluation runner.

               -  **Parameters:** Individual parameters depending on the
                  type oe evaluation. When plotting transfer
                  characteristics:

                  -  e.g. for CNT PUF raw evaluation
                  .. code-block:: json
                  
                     {"scale": "linear", "hide_legend": "false", "legend_font_size": 20, "axis_tick_font_size": 15,
                     "axis_label_font_size": 20, "title_font_size": 20, "plot_mode": "Source Drain Current"}

               -  **Returns:**
               .. code-block:: json

                  {"status": "ok"}
                  {"status": "error"}

            -  **GET /evaluation/get_status** returns the status of all
               evaluation runs.

               -  **Returns:**
               .. code-block:: json

                  {"tasks": [{"task_id": 158, "id": 158, "title": "Test", "startTime": 1706474333358.4011, 
                  "stopTime": 1706474385709.7869, "status": "finished", "evaluationType": "waferVisualizer"}]}

            -  **DELETE /evaluation/delete_result** deletes an
               evaluation result from the database.

               -  **Parameters:**

                  -  taskID: id of the task to delete.

               -  **Results:**
               .. code-block:: json

                  {"status": "ok"}
                  {"status": "error"}

            -  **GET /evaluation/visualizations** returns evaluation
               data and a visualization json corresponding to a certain
               taskID.

               -  **Parameters:** taskID: id to identify the chart and
                  evaluationStatus data.
               -  **Results:**

                  -  Returns a test specific chart and evaluationStatus
                     data object.

-  .. rubric:: Generic Messaging Service
      :name: generic-messaging-service

   Provides all the functionality to communicate with a messaging
   service. Currently, NATS messaging service is implemented, which
   allows to discover devices and to schedule test to multiple Micro
   Service which implements the device specific interface.

   -  It provides the following endpoints:

      -  **GET /nats/start** starts the nats service and connects to the
         broker (Important: run nats-server bevore)

         -  **Returns:**:

         .. code-block:: json

            {"status": "started"}    
            {"status": "running"}
            {"status": "error"}

      -  **GET /nats/get_test_status** returns a list of all waiting,
         running or finished tests and additional data such as the test
         title, current, iteration, etc.

         -  **Parameters:**:

            -  filter: specifies the queue which filters “waiting”,
               “running” or “finished” tests.

         -  **Returns:**:

         .. code-block:: json

            {"status": "ok"}
            {"status": "error"}

      -  **POST /nats/schedule_test** schedules a test across the
         nats-broker.

         -  **Parameters:**

            -  test specifying the specification in json

         -  **Returns:**

         .. code-block:: json

            {"status": "ok"}
            {"status": "error"}

-  .. rubric:: Test Manager
      :name: test-manager

   Provides models and functionality to store and filter test templates
   and instances.

   -  It provides the following endpoints:

      -  **GET /tests/get_evaluated_data** returns evaluation data
         filtered by its type and id.

         -  **Parameters:**

            -  type: defines the test category either “cnt_puf” or
               “memory” is currently supported
            -  id: Identifier of the test of a specific test category

         -  **Returns:**

            .. code-block:: json

               {"status": "ok"}
               {"status": "error"}

      -  **GET /tests/get_default_values** returns the default values of
         a “memory” or “cnt_puf” test template initiation.

         -  **Parameters:**

            -  testClass: defines the test category either “cnt_puf” or
               “memory” is currently supported.

         -  **Returns:**

            -  in case of cnt_pufs

               .. code-block:: json

                  {"title": "", "min_VDS": -1, "max_VDS": 1, "step_VDS": 0.1,
                   "min_VGS": -2.5, "max_VGS": 2.5, "step_VGS": 0.1, "test_type": "",
                   "nrIterations": 1, "pulsed": "False", "temperature": 20, "hysteresis": "False"}

      -  **GET /tests/get_test_categories** returns the different test
         categories available, e.g. memory tests, cnt, script or
         memristor tests.

         -  **Returns:**
         .. code-block:: json

            {"categories": [{"field": "memoryTest", "name": "Memory Test"}, {"field": "cntTest", "name": "Carbon Nanotube Test"},      
            {"field": "memristorTest", "name": "Memristor Test"}, {"field": "scriptExecution", "name": "Script Test"}]}

      -  **POST /tests/add_test** add a test template to the database,
         which can later be scheduled.

         -  **Parameters:**

            -  parameter expects a json with test template specific
               parameters, e.g. for cnt-pufs

               .. code-block:: json

                  {"title": "test", "test_type": "TransferCharacterization", "nrIterations": 2, min_vDS: -0.5,
                   "max_VDS": 0.5, "....."}

         -  **Returns:**
           .. code-block:: json

               {"status": "ok"}
               {"status": "error"}

      -  **DELETE /tests/delete_test** deletes a test template
         identified by the test category and identifier.

         -  **Parameters:** testType: defines the test category either
            “cnt_puf” or “memory” is currently supported id: Identifier
            of the test of a specific test category
         -  **Returns:**
           .. code-block:: json

               {"status": "ok"}
               {"status": "error"}

      -  **GET /tests/get_tests** returns a list of test templates
         filtered by the test type.

         -  **Parameters:** testType: defines the test category either
            “cnt_puf” or “memory” is currently supported
         -  **Returns:**

            .. code-block:: json
               
                {"tests":[{"id": 1, "title": "test", "testType": "Read Latency Tests", "category": "memory", "initialValue": "0", "startAddress": 0.0,
                "stopAddress": 0.0, "voltage": 10.0, "temperature": 10.0, "dataSetupTime": "1", "createdAt": "None", "iterations": 1, "initialValue_2": "1"}]}




