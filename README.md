# znc oneway relay

znc module to create oneway relays for channels you'd like to mirror 

## limitation:
you can't specify a source network to relay from, only a channel name. if you're
in two channels w/ the same name on separate networks, it will relay both.

this is a limitation in znc. if you know a way to get around this, create an
issue or pull request on github.

## commands
| command | description            | example                            
| ---     | ---                    | ---                                
| help    | show this help message | help                               
| add     | add a relay            | add #znc privatenetwork #znc-relay 
| del     | delete a relay         | del 0                              
| list    | list all relays        | list                               
