#! /usr/bin/env bash

pushd `dirname $0`

pdflatex -output-directory=output -file-line-error -shell-escape -interaction=nonstopmode report.tex | egrep ".*:[0-9]*:.*|.*Warning:"
#if [[ $? == 0 ]]; then
#  unamestr=`uname`
#  if [[ "$unamestr" == 'Linux' ]]; then
#    gnome-open output/report.pdf >& /dev/null
#  #elif [[ "$unamestr" == 'Darwin' ]]; then
#  #  open output/report.pdf
#  fi
#fi
