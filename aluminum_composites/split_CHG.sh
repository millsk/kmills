#!/bin/bash

awk '$1=="undoped_hotter" {n++}{print > "CHG"n }' CHG


