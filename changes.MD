# Changes for WEB
1. Charts min update time set to 200ms **OK**
2. Charts configuration request /confgraph?n=graphID&choix=[abcdefghij...] 1<=graphID<=14 **OK**
3. EventSource : single event EventSource("events/")  **OK**
   "CAP_readings2"=>"CAP_reading_graph"
   "CAP_readings3"=>"CAP_reading_index"
   "CAP_readings"=>"CAP_reading_cons"
   "TEST_readings"=>"AUTOTEST_reading"
   
   "fct_fin"=>"DEMAG_fin"

4. Session management : /ouvpage => user started the session /deconnect => Session closed **OK**
5. Variables name : no more varX **OK**
6. JSON exchanges : only relevant data (according to configs) **OK**
7. EN/FR support (/setlanguage=[fr|en])