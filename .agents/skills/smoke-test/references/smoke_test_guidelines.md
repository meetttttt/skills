# Smoke Test Implementation Patterns by Framework

This reference guide provides code patterns for generating clean, isolated, fast-executing smoke test suites across popular languages and frameworks.

---

## 1. JavaScript / TypeScript (Jest / Vitest)

File location: `tests/smoke/feature.smoke.test.ts` or `src/__tests__/smoke.test.ts`

```typescript
import { slugify } from '../../src/utils';

describe('Smoke Test Suite: Slugify Utility Requirements', () => {
  it('REQ-1: Preserves non-Latin UTF-8 unicode characters', () => {
    expect(slugify('Hello 世界')).toBe('hello-世界');
    expect(slugify('Café y Música')).toBe('café-y-música');
  });

  it('REQ-2: Strips punctuation and replaces whitespace with single dashes', () => {
    expect(slugify('  Hello!!!   World???  ')).toBe('hello-world');
  });

  it('REQ-3: Handles edge cases (null, empty strings, zero values)', () => {
    expect(slugify('')).toBe('');
    expect(slugify(null as any)).toBe('');
  });
});
```

---

## 2. Python (pytest)

File location: `tests/test_smoke_feature.py`

```python
import pytest
from src.utils import slugify

class TestSlugifySmokeSuite:
    """Smoke test suite validating slugify function requirements."""

    def test_req1_utf8_unicode_preservation(self):
        assert slugify("Hello 世界") == "hello-世界"
        assert slugify("Café y Música") == "café-y-música"

    def test_req2_punctuation_stripping(self):
        assert slugify("  Hello!!!   World???  ") == "hello-world"

    def test_req3_boundary_inputs(self):
        assert slugify("") == ""
        assert slugify(None) == ""
```

---

## 3. HTTP / REST API Smoke Scripts (cURL / Bash)

File location: `tests/smoke/api_smoke.sh`

```bash
#!/usr/bin/env bash
set -e

BASE_URL="${API_URL:-http://localhost:3000}"

echo "=== Running API Smoke Test Suite against ${BASE_URL} ==="

# REQ-1: Health Check Endpoint
echo -n "Test 1: GET /health ... "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" "${BASE_URL}/health")
if [ "$STATUS" -eq 200 ]; then
  echo "PASS (200 OK)"
else
  echo "FAIL (Status $STATUS)"
  exit 1
fi

# REQ-2: POST /api/v1/resource Validation
echo -n "Test 2: POST /api/v1/resource (Invalid payload) ... "
STATUS=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${BASE_URL}/api/v1/resource" -H "Content-Type: application/json" -d '{}')
if [ "$STATUS" -eq 400 ]; then
  echo "PASS (400 Bad Request)"
else
  echo "FAIL (Status $STATUS)"
  exit 1
fi

echo "=== All API Smoke Tests Passed Cleanly ==="
```

---

## 4. Go (`go test`)

File location: `smoke_test.go`

```go
package main

import (
	"testing"
)

func TestSlugifySmoke(t *testing.T) {
	tests := []struct {
		name     string
		input    string
		expected string
	}{
		{"REQ-1: UTF8 Preserved", "Hello 世界", "hello-世界"},
		{"REQ-2: Punctuation Strip", "Hello!!! World???", "hello-world"},
		{"REQ-3: Empty Input", "", ""},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			result := Slugify(tt.input)
			if result != tt.expected {
				t.Errorf("Slugify(%q) = %q; want %q", tt.input, result, tt.expected)
			}
		})
	}
}
```
