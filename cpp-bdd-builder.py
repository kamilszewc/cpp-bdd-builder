#!/usr/bin/env python3
"""
Script to generate catch2 or gtest test files from a yaml description.
Author: Kamil Szewc, License: BSD 3-clause
"""

import argparse
import re
import yaml


class Header:
    """Represents tests header"""
    def __init__(self, spec):
        self.spec = spec

    def parse(self, framework):
        if framework == "gtest":
            return "#include <gtest/gtest.h>\n"
        else:
            return "#include <catch2/catch_test_macros.hpp>\n"


class Title:
    """Represents tests title"""
    def __init__(self, spec):
        self.spec = spec

    def parse(self, framework):
        return "// Title: " + self.spec["title"] + "\n"


class AsA:
    """Represents tests 'as a' description"""
    def __init__(self, spec):
        self.spec = spec

    def parse(self, framework):
        return "// As a: " + self.spec["as-a"] + "\n"


class IWant:
    """Represents tests 'I want' description"""
    def __init__(self, spec):
        self.spec = spec

    def parse(self, framework):
        return "// I want: " + self.spec["i-want"] + "\n"


class SoThat:
    """Represents tests 'so that' description"""
    def __init__(self, spec):
        self.spec = spec

    def parse(self, framework):
        return "// So that: " + self.spec["so-that"] + "\n"


def parse_scenario_gtest_name(name):
    """Parse scenario name to form acceptable by gtest"""
    # strip
    name = name.strip()
    # space and tab to _
    name = name.replace(" ", "_").replace("\t", "_")
    # remove dots. commas
    name = re.sub('[^a-zA-Z_]+', '', name)
    # make lower
    name = name.lower()
    return name


class Scenario:
    """Represents scenario"""
    def __init__(self, scenario, group):
        self.scenario = scenario
        self.group = group

    def __parse_scenario_gtest_name(name):
        """Parse scenario name to form acceptable by gtest"""
        # strip
        name = name.strip()
        # space and tab to _
        name = name.replace(" ", "_").replace("\t", "_")
        # remove dots. commas
        name = re.sub('[^a-zA-Z_]+', '', name)
        # make lower
        name = name.lower()
        return name

    def parse(self, framework):
        if framework == "gtest":
            return "TEST(" + self.group + ", " + self.__parse_scenario_gtest_name(self.scenario["scenario"]) + ")\n"
        else:
            return "SCENARIO( \"" + self.scenario["scenario"] + "\", \"[" + self.group + "]\")\n"


class Given:
    """Represents 'given' statement"""
    def __init__(self, scenario):
        self.scenario = scenario

    def parse(self, framework):
        if framework == "gtest":
            return "    // Given " + self.scenario["given"] + "\n"
        else:
            return "    GIVEN( \"" + self.scenario["given"] + "\")\n"


class When:
    """Represents 'when' statement"""
    def __init__(self, scenario):
        self.scenario = scenario

    def parse(self, framework):
        if framework == "gtest":
            return "        // When " + self.scenario["when"] + "\n"
        else:
            return "        WHEN( \"" + self.scenario["when"] + "\")\n"


class Then:
    """Represents 'then' statement"""
    def __init__(self, scenario):
        self.scenario = scenario

    def parse(self, framework):
        if framework == "gtest":
            return "            // Then " + self.scenario["then"] + "\n"
        else:
            return "            THEN( \"" + self.scenario["then"] + "\")\n"


class CppBddBuilder:
    """Class generate catch2 or gtest test files from a yaml description"""
    def __init__(self, filename, group):
        self.group = group

        with open(filename) as file:
            self.spec = yaml.load(file, Loader=yaml.FullLoader)

    def get_spec(self):
        return self.spec

    def generate(self, framework):
        output = ""

        output += Header(self.spec).parse(framework)
        output += Title(self.spec).parse(framework)
        output += AsA(self.spec).parse(framework)
        output += IWant(self.spec).parse(framework)
        output += SoThat(self.spec).parse(framework)
        output += "\n"

        for scenario in self.spec["scenarios"]:
            output += Scenario(scenario, self.group).parse(framework)
            output += "{\n"
            output += Given(scenario).parse(framework)
            output += "    {\n"
            output += "        // Type code here\n\n"
            output += When(scenario).parse(framework)
            output += "        {\n"
            output += "            // Type code here\n\n"
            output += Then(scenario).parse(framework)
            output += "            {\n"
            output += "                // Type code here\n"
            output += "            }\n"
            output += "        }\n"
            output += "    }\n"
            output += "}\n\n"

        return output


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    parser.add_argument("--framework", default="catch2")
    parser.add_argument("--group", default="default")
    args = parser.parse_args()

    cppBddBuilder = CppBddBuilder(args.filename, args.group)
    print(cppBddBuilder.generate(args.framework))
