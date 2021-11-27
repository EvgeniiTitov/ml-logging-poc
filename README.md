Quick POC

User doing an ML experiment (model training, inference or whatever) imports the
package.

User instantiates an object representing a running experiment -> Run

The Run object must support the following functionality

- Pushing metadata (pretty much anything we deem useful) to the server

- Pulling objects from the server

Pushing could be done async -> Streamer object sitting in a thread

Pulling could be done either sync or async. Sync makes more sense 


Issues:
1. If user code exits earlier, we might not have time to push stuff 
to the backend