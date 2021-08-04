# Architecture

1. 기존의 실행 구조: start_clipper.py -> clipper/course_save.py -> *site*.py
2. 문제점: 
    - 수집을 모두 마치고서야 비로소 db저장을 하게 되므로 메모리 사용이 많다.
    - 중간에 에러가 발생할 경우 db저장은 하나도 못하게 된다.
3. 새로운 실행 구조의 요건:
    - page별 수집-db저장 을 수행한다.
    - 어떤 강좌를 수집하고 저장하는지 화면에 출력한다.
4. 새로운 실행 구조를 짜는 전략:
    - start_clipper.py 에서 실행명령을 내리면,
    - 개별 사이트가 타겟이 되어 개별사이트에 해당하는 모듈(eg. inflearn.py)이 호출된다.
        (기존에는 course_save.py를 호출했다.)
    - 그 사이트 모듈은 실행 세분화를 해주는데 
        1) 사이트 특성에 맞는 수집방법을 골라 수행하고, 수집된 정보의 structure는 동일하므로
        2) import한 공통 세이빙모듈(eg. course_save.py)로 db에 저장하되
        3) **한 차례 저정용량을 지정할 수 있도록 한다.**
        
5. 필요한 기능:
    - saving interval / pause / resume
    - 