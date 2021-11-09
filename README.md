### Install & usage
You need docker and docker-compose installed on your machine to run this project.

From root directory run:
`
docker-compose up --build
`

After a few second you will se results coming from 'position server'.


### Roadmap / possible improvements
- Add more tests
- Improve API documentation
- Add better error/exceptions handling
- Consider security like authorization
- Use better aproach to comunication between services (tool like Kafka might be a good choice)
- Use environment variables to pass configuration
- Consider corner cases (AUM response might be available after trade fill is received in controller)
- Improve logging and verbosity
- Split services into separate repositories