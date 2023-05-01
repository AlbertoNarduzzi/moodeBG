#!/bin/bash

function main()
{
    ./node_modules/.bin/gulp build --force
    if [ 0 == $? ]; then
    {
        sudo ./node_modules/.bin/gulp deploy --force
    }
    fi;
}

main "$@";
