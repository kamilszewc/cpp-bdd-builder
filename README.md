# cpp-bdd-builder

Very basic script to generate catch2 or gtest test files from a yaml description.

`usage: cpp-bdd-builder.py [-h] [--framework FRAMEWORK] [--group GROUP] filename`

where GROUP is a test group (any name), while FRAMEWORK can be one of two options: catch2 (default) or gtest.

Example input file:
```yaml
title: Returns and exchanges go to inventory.
as-a: As a store owner,
i-want: to add items back to inventory when they are returned or exchanged,
so-that: I can track inventory.

scenarios:
  - scenario: Items returned for refund should be added to inventory.
    given: that a customer previously bought a black sweater from me
    when: they return the black sweater for a refund,
    then: I should have four black sweaters in inventory.
```

Catch2 result:
```c
#include <catch2/catch_test_macros.hpp>
// Title: Returns and exchanges go to inventory.
// As a: As a store owner,
// I want: to add items back to inventory when they are returned or exchanged,
// So that: I can track inventory.

SCENARIO( "Items returned for refund should be added to inventory.", "[default]")
{
    GIVEN( "that a customer previously bought a black sweater from me")
    {
        // Type code here

        WHEN( "they return the black sweater for a refund,")
        {
            // Type code here

            THEN( "I should have four black sweaters in inventory.")
            {
                // Type code here
            }
        }
    }
}
```

Gtest result:
```c
#include <gtest/gtest.h>
// Title: Returns and exchanges go to inventory.
// As a: As a store owner,
// I want: to add items back to inventory when they are returned or exchanged,
// So that: I can track inventory.

TEST(default, items_returned_for_refund_should_be_added_to_inventory)
{
    // Given that a customer previously bought a black sweater from me
    {
        // Type code here

        // When they return the black sweater for a refund,
        {
            // Type code here

            // Then I should have four black sweaters in inventory.
            {
                // Type code here
            }
        }
    }
}

```