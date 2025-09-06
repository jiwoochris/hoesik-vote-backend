---
description: 'Pytest E2E testing standards'
applyTo: '**/*.py'
---

# pytest 기반 테스트 코드 작성 방법

## E2E 테스트 전략

본 프로젝트는 **사용자 시나리오 기반 E2E 테스트**만을 사용합니다. 단위 테스트는 하지 않고, 실제 사용자 여정을 검증하는 인수 테스트에 집중합니다.

### 핵심 원칙
- **단위 테스트 금지**: Service나 Repository 계층의 격리 테스트는 작성하지 않습니다
- **완전한 사용자 여정**: API부터 DB까지 전체 스택을 통합 테스트합니다
- **실제 비즈니스 시나리오**: 사용자가 실제로 경험하는 워크플로우만 테스트합니다

## TDD

본 프로젝트는 TDD(Test-Driven Development) 방식을 따릅니다. 새로운 기능을 추가하거나 버그를 수정하기 전에 반드시 테스트 케이스를 먼저 작성해야 하며, 모든 테스트는 `pytest`를 사용하여 실행합니다.

- 항상 "Red - Green - Refactor" 순서로 개발을 진행하세요.
- 최대한 유저 시나리오를 기반으로 구체적으로 테스트 케이스를 작성합니다.
- Test 함수명 아래에 docstring을 작성하여 테스트의 목적과 기대 결과를 명확히 합니다.
- conftest.py에 fixture(autouse=True)를 사용하여 테스트 전후에 필요한 초기화 작업을 수행합니다.
- 아래와 같이 Given-When-Then 패턴을 사용하여 테스트 케이스를 작성합니다.

```
def test_menu_list_empty():
    """
    메뉴가 없을 때 빈 리스트를 반환해야 한다.
    """
    # Given: 데이터베이스에 메뉴가 없는 상태

    # When: /api/menus 엔드포인트에 GET 요청을 보낸다
    response = client.get("/api/menus")

    # Then: 200 OK와 빈 리스트가 반환된다
    assert response.status_code == 200
    assert response.json() == []
```