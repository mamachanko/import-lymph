# `import lymph`

Welcome to the materials and the transcript of an introduction to
[lymph](http://lymph.io). Lymph is a framework for writing services in Python.

## Playground setup

We've got a [vagrant](http://vagrantup.com) box for you, if you want to follow along
the talk or simply play around with services. We suggest to use, but local
setup should be straightfoward as well.

The box is set up with all tooling and code ready for your perusal. It has both
[Zookeeper](http://zookeeper.apache.org/) and
[RabbitMQ](https://www.rabbitmq.com/) running inside. Getting inside the box is
a matter of running:

```shell
vagrant up && vagrant ssh
```

You will be prompted for your root password half-way through `vagrant up`
because we use NFS to share files.

Once inside the box, the `motd` contains more information on what's available.
However, the box simply provides to the tmux sessions we use in the talk to
explore lymph and its tooling.

## The talk
> An introduction to lymph by Alejandro Castillo & Max Brauer

### Opening

Hello, we'd like to introduce you to [lymph](http://lymph.io) a framework for
writing services in Python. With lymph you can write services with almost no
boilerplate. But let me introduce us first.

We're [Delivery Hero](http://deliveryhero.com), a holding of online
food-ordering services. We're located in Berlin. We operate in 34 countries
and growing.

Let me explain the concept of online food-ordering to those who're unfamiliar
with it. However, I doubt this is news to anyone, The concept is simple:
* get hungry
* go online
* search for restaurants close to you
* compile your order
* pay online
* wait for the delivery
Basically, it's e-commerce with very grumpy customers. Nonetheless, the
restaurant integration, e.g. order transmission, fulfillment, delivery, etc.
offer quite an ecosystem of things to tackle.

What are we going to talk about? Let's briefly go over the flow of our talk:
1. We're going to explain where we're coming from and why we have given birth
   to a(nother) framework
1. We'll look at code as fast possible
1. We'll run services and increasingly add new services to explore communication
   patterns and the tooling of lymph
1. We'll briefly talk about how lymoh does things under the hood
1. We'll touch on similar technology and how it relates to lymph (Nameko in
   particular)
1. We'll talk future plans for lymph and its ecosystem
1. That's it :)

For the sake of this talk we assume that you're familiar with the concept of
services. We assume that you are familiar with what a monolith is. We assume
that you are familiar with when and why to use either and even more so when
not. We will not discuss the differences between monoliths and services. We
won't talk about how services might safe your development or your business.
Neither will we talk about sophisticated networking topologies.

But what we're going to talk about is lymph. By the end of the talk you should
understand what lymph can and cannot do and why that's cool. If you achieved
that we consider ourselves succesful.

You can find all material and a transcript of this talk
[online](http://mamachanko.github.io/lymph-talk).

If you speak Spanish then you may also want to attend [this very
talk](https://ep2015.europython.eu/conference/talks/deja-de-pegarte-con-tus-servicios-import-lymph)
in Spanish later this week by Castillo.

If you happen to attend the PyCon France, we'll be ther too.

Also, you can find us at our sponsor table in the foyer. We've brought goodies
and gummi bears.

(repeat all this in the end)

### Motivation

Our initial situation was the classic one. We had a massive Django monolith.
We weren't moving fast at all. We've had trouble finding rhythm for a growing
number of teams and developers. People we're blocked by other people. The code
base was a big bowl of legacy spaghetti. We've had issues scaling. You should
think of the textbook situation "my monolith hurts, i want services". So, the
idea of a more service-oriented architecture became increasingly reasonable to
us.  Another dimension is our heterogenic product landscape. While most
countries websites work the same they always differ in some aspects. Modularity
was key for us.

The first thing some of you would think is 'why write another
framework?'. The answer is that when we looked around we did not find
anything that would fit our needs. We wanted to work with services but we
wanted some very specific things(@TODO what are these?). We are mainly
Python-powered so we wanted to stay inside Python as much as possible. We
wanted to abstract away all the problems one is dealing with when doing
services. That is, developers are not supposed to worry about transporting
data, registering services, discovering them etc. We wanted to enable our
developers to work with services in a simple and easy way: as little
boilerplate as possible, no details that don't relate to bussiness logic.

We're ging to talk about related technoglogies later.


Yes, some of you will be thinking after their nice talk 'use Nameko'. But that
was not in the current state when we started. It also does not cover all the
things we wanted to get from a framework.

Quick show of hands, how many of you attended Matt's talk about
[nameko](https://github.com/onefinestay/nameko)??  Nevermind though, we'll
briefly touch on Nameko later.

But finally, say hello to [lymph](http://lymph.io). By now, hopefully, you're
itching to see how a service looks in lymph. Spoiler alert: very much like in
nameko.

We'll break the ice by demoing running and playing around with services. We'll
slowly progress through lymph's features, service by service.

### Demo

#### The greeting service

[This](services/greeting.py) is what a simple greeting service looks like in
lymph. Its interface is one RPC method called `greet` which takes a name,
prints it, emits an event(containing the text in the body) and returns a
greeting for the given name.

```python
import lymph


class Greeting(lymph.Interface):

    @lymph.rpc()
    def greet(self, name):
        print('Saying hi to %s' % name)
        self.emit('greeted', {'name': name})
        return u'Hi, %s!' % name
```

All we need to do to make things happen is to inherit from `lymph.Interface`
and decorate RPC methods with `@lymph.rpc()`. Lastly, we've got the interface's
`emit()` function to our disposal which dispatches events in the event system.

Let's jump on the shell and play with it.

``` shell
» mux start greeting
```

What you see here is a tmux session with two panes. On the right-hand side you
see the greeting service being run with lymph's `instance` command. On the
left-hand side you see a plain shell on which we'll explore lymph's tooling.

Every time you want to run an instance of a servcie you need to point lymph to
its configuration. The configuration tells lymph about the interface's name and
where it can import it from. Since lymph imports the interface, its modulea
needs to be on the `PYTHONPATH`. Why can make this happen with `export
PYTHONPATH=services` in our example. But worry not, the tmuxinator sessions
take care of it for you. Our service's configuration looks like
[this](conf/greeting.yml):

```yaml
interfaces:
    Greeting:
        class: greeting:Greeting
```

The `lymph instance` command receives the path to this file.

One of the first things we considered when building lymph was the tooling. We
think we managed to get some very nice tooling built around it to make
development of services easier.

So what tooling is available? `lymph list` will tell us.

``` shell
» lymph list
```

You see there's plenty of commands available to interact with services.

To begin with let's assert that an instance of the echo service is running.
We'll use lymph's `discover` command.

``` shell
» lymph discover
Greeting [1]
```

As you can see, one instance is running indeed (`Greeting [1]`).

Let's excercise the service's `greet` method. We'll use lymph's `request`
command. Therefore, we have to provide the service name, the name of the method
and the body of the request as JSON. What we expect to see is the echo service
to return the text as is, but it should also print it and emit an event.

```shell
» lymph request Greeting.greet '{"name": "Joe"}'
u'Hi, Joe!'
```

The result of the RPC is `'Hi, Joe!'` as expected and the service printed the
name.

This is boring and our service must be pretty lonely. Nobody listens to its
events. Here comes a listener.

#### The listen service

The [listen service](services/listen.py) listens to greeting's events Again,
it's a lymph service(we inherit from `lymph.Interface`). However, there's
nothing but one method which is subscribed to `greeted` events. It simply
prints the greeted name contained in the event's body. Everytime an event of
this type occurs exactly once instance of the listen service will consume it.

```python
import lymph


class Listen(lymph.Interface):

    @lymph.event('greeted')
    def on_greeted(self, event):
        print('Somebody greeted %s' % event['name'])
```

Let's excercise our services combination. This time round, though, we'll run
two instances of the greeting service and one instance of the listen service.

The [listen service's configuration](conf/listen.yml) is no different from the
one before.

``` shell
» mux start greeting-listen
```

Again, we see a tmux session. On the right you find two instances of the
greeting service followed by an instance of the listen service.

We should find them registered correctly.

``` shell
» lymph discover
Greeting [1]
Listen [1]
```

And, indeed, they list correctly.

Let's emit a `greeted` event in the event system to assert whether the listen
service listens to it. We'll use lymph's `emit` command. We're expecting the
listen service to print the name field from the event body.

```
» lymph emit echo '{"greeted": "Joe"}'
```

Nice. That worked.

When we do RPCs now we expect the greeting instances to respond in round-robin
fashion while the listen instance should rect to all occuring events.

``` shell
» lymph request Greeting.greet '{"name": "Joe"}'                                │
u'Hi, Joe!'
```
(do this repeatedly, until both greeting instances have responded)

As you see, our expectations are met.

If we were to run several instances of the listen services, each event would be
consumed by exactly once instance. However, lymph allows to broadcast events.

Finally, since it's 2015, no talk would be complete without talking about HTTP.
Let's add a web service to the mix. Let's say we wanted to expose the greeting
functionality via an HTTP API. Lymph has a class for that.

#### The web service

[This](services/web.py) is the Web service. It subclasses lymph's
`WebServiceInterface`. In this case we're not exposing RPC methods, emitting
not listening to events. However, we configure a Werkzeug URL map as a class
attribute. We've added one endpoint: `/greet` and a handler for it. The handler
receives a Werkzeug request object.

```python
from lymph.web.interfaces import WebServiceInterface
from werkzeug.routing import Map, Rule
from werkzeug.wrappers import Response


class Web(WebServiceInterface):

    url_map = Map([
        Rule('/greet', endpoint='greet'),
    ])

    def greet(self, request):
        name = request.args['name']
        print('About to greet %s' % name)
        return Response(
            self.proxy('Greeting').greet(name=name)
        )
```

The greet handler expects a name to be present in the query string. It calls
the greeting service via the `self.proxy` and returns the result in the
response. And it prints.

Mind, that we're not validating the request method nor anything else.

Run it or it didn't happen, they say. We'll bring up an instance of each of
services now.

Once more, the [web service's configuration](conf/web.yml) is no different from
the ones we looked at before.

``` shell
» mux start all
```

On the right you can see an instance of every service: web, greeting and
listen.

Once again, they should have registered correctly:

``` shell
» lymph discover
Web [1]
Greeting [1]
Listen [1]
```

Let's hit our web service and see how the request penetrates our service
landscape. We should see all service print something. The web service is
listening at the default port 4080. We're using `httpie` to excercise the
request:

```
» http localhost:4080/greet?name=joe
HTTP/1.1 200 OK
Content-Length: 8
Content-Type: text/plain; charset=utf-8
Date: Fri, 03 Jul 2015 13:55:29 GMT

Hi, joe!
```

The response looks good and all services should have performed accordingly.

#### Lymph's development server

Yet, when developing locally you seldomly would want to run all of your
services within different shell or tmux panes. Lymph has its own development
server which wraps around any number of services with any number of instances
each. Therefore, we'll have to configure which services to run and how many
instances of each in the [`.lymph.yml`](.lymph.yml):

```yaml
instances:
    Web:
        command: lymph instance --config=conf/web.yml
        numprocesses: 2

    Greeting:
        command: lymph instance --config=conf/greeting.yml
        numprocesses: 3

    Listen:
        command: lymph instance --config=conf/listen.yml
        numprocesses: 4


sockets:
    Web:
        port: 4080
```

(Since we run several instances of our web service we have to configure shared
sockets.)

Mind that in our case `command` specifies lymph instances but this could also
be any other service you need, e.g. Redis.

Let's bring them all up.

``` shell
» mux start all
```

Once more, we find ourselves inside a tmux session with lymph node running in
the top-right pane. Below that you see `lymph tail` running which allows us to
follow the logs of any number of services. But first, let's check how many
instances are running:

``` shell
» lymph discover
Web [2]
Greeting [3]
Listen [4]
```

That's a good number. Once we feed a request into the cluster we should see
print statements and logs appearing.

``` shell
» http localhost:4080/greet?name=joe
HTTP/1.1 200 OK
Content-Length: 8
Content-Type: text/plain; charset=utf-8
Date: Fri, 03 Jul 2015 13:55:29 GMT

Hi, joe!
```

There's a lot going on in the tail pane. You would find an even bigger mess the more
services and instances you run and the more intricated your patterns of
communication become. Sometimes you wonder "where did my request go?". Lymph
helps you though with `trace\_id`s. Every request that appears in our cluster
which doesn't have a trace id assigned gets one. These trace ids get fowarded
via every RPC and event.

So we should be able to corellate all actions in cluster to the one incoming
HTTP request. If you check the logs within the tail pane you should see that
all logs can be related with the `trace_id`. And indeed we see the same
`trace_id` across our service instances for every incoming request.

[use iterms highlighting: Ctrl+f and type 'trace_id']

That mostly covers the tooling we have for lymph services. Let's talk about
lymph's stack next.

#### Things we haven't touched
* lymph subscribe
* lymph shell
* config API
* on_start
* metrics
* plugins (new relic, sentry, lymph-top)

### Lymph under the hood

How does lymph do things under the hood?

* greenlets
* rpc via 0mq
* events via rabbitmq (pluggable)
* registry via zk (pluggable)
* http with werkzeug
* testing

### Lymph compared to other "frameworks"
Nameko
* (http://lucumr.pocoo.org/2015/4/8/microservices-with-nameko/)
* tech
* running
* testing
* only rabbitmq, no zk

zerorpc, cocaine, spread, crossbar, circuits, iPOPO, ...

### Future
* eco system (storage, storeproxy, flow etc)
* distconfig

### Summary & outro
* did we accomplish? circle back to claim and title
* lymph.io
* we accept PRs
* we're hiring
* same talk in Spanish
* PyCon Fr

### Q&A
* why zookeeper for registry?
* how to scale up web services? (sharing sockets)
 
### Nice to have
* plugins (lymph-top, newrelic, sentry)
* monitoring
* serial events & broadcast(websockets)
* sieve of Erathostenes (Mislav)
