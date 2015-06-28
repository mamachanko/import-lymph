# Stop trying to glue your services together`; import lymph`

## Setup

It is suggest to use the provided vagrant box. It's setup with all tolling and
code ready for your perusal. To get it up and running:

``` shell
vagrant up && vagrant ssh
```

You will be prompted for the root password half-way through `vagrant up`
because we use NFS to share files.

Once inside, the `motd` contains all information you need to play around.

## The talk
> A talk for EuroPython 2015 by Alejandro Castillo & Max Brauer

Hello and good afternoon. Hopefully you've had a nice lunch. My name is
<name> and I'd like to introduce you to _lymph_, a framework for
writing services in Python. With lymph you can write services with almost no
boilerplate. But let me introduce us first.

We're Delivery Hero, a holding of online food ordering services world-wide.
We're located in Berlin. We operate in 34 countries and growing. Let me
explain the concept of online food ordering to those who're unfamiliar with it.
However, I doubt there arent any ;) The concept it's simple: get hungry, go
online, search for restaurants close to you, compile your order, pay online,
wait for the delivery. Basically, it's e-commerce with very grumpy customers.
But the restaurant integration, e.g. order transmission, fulfillment, delivery,
etc. offer quite an ecosystem of things to tackle.

Let's briefly go over the flow of our talk:
* We're going to explain where we're coming from and why we have given birth
  to another framework
* We'll look at code as fast possible
* We'll run services and increasingly add new services to explore communication
  patterns and characteristics of lymph
* We'll give you a brief rundown of lymph's internal
* We'll go over how lymph is different from nameko
* We'll talk future plans

For the sake of this talk we assume that you're familiar with the concept of
services. We will not discuss the differences between monoliths and services.
We assume you are familiar their characteristics.

By the way, how many of you have attended the nice talk about
[nameko][https://github.com/onefinestay/nameko]?

Our starting point was the classic situation. We had a massive Django monolith.
We weren't moving fast at all. We've had trouble finding rhythm for a growing
number of teams and developers. The perks of a more service-oriented became
increasingly attractive and reasonable to us. This was even more so in the
light of a global platform to unite our very heterogenic Product landscape.

So, the first thing some of you would be thinking is 'why write another
framework?'. The answer was that when we looked around we did not find
anything that would fit our needs. We wanted to work with services but we
wanted some very specific things(@TODO what are these?). We are mainly
Python-powered so we wanted to stay inside Python as much as possible. We
wanted to abstract away all the problems one is dealing with when doind
services, i.e. transport data, register services, discover them etc. We wanted
to enable our developers to work with services in a simple and easy way: no
boilerplate, no excessive details that don't relate to bussiness logic.

@TODO: prepare other alternatives and related technologies and possible go over
them (jsonrpc, zerorpc, chaussette, cocaine, ...)

Yes, some of you will be thinking after their nice talk 'use Nameko'. But that
was not in the current state when we started. It also does not cover all the
things we wanted to get from a framework. Nevermind though, we'll briefly go
over the differences of the two later.

So, say hello to [lymph][lymph.io]. By now, hopefully, you're itching to
see how a service looks in lymph. Spoiler alert: very much like in nameko.

We'll break the ice by demoing running and playing around with services. We'll
slowly progress through lymph's features, service by service.

[show Echo service code]

### Demo

Et voila. This is what a simple echo service looks like in lymph. Its interface
is one RPC method called `echo` which takes text, prints it, emits an
event(containing the text in the body) and returns the text.

All we need to do to make things happen is to inherit from `lymph.Interface`
and decorate RPC methods with `@lymph.rpc()`. Lastly, we've got the interface's
`emit()` function to our disposal which dispatches events in the event system.

Let's jump on the shell and play with it.

``` shell
mux start echo
```

What you see here is a tmux session with two panes. On the right-hand side you
see the echo service being run with lymph's `instance` command. On the
left-hand side you see a plain shell on which we'll explore lymph's tooling.

One of the first things we considered when building lymph was the tooling. We
think we managed to get some very nice tooling built around it to make
development of services easier.

So what tooling is available? `lymph list` will tell us.

``` shell
lymph list
```

You see there's plenty of commands available to interact with services.

To begin with let's assert that an instance of the echo service is running.
We'll use lymph's `discover` command.

``` shell
lymph discover
```

As you can see, one instance is running indeed (`Echo [1]`).

Let's excercise the echo service's `echo` method. We'll use lymph's `request`
command. Therefore, we have to provide the service name, the name of the method
and the body of the request as JSON. What we expect to see is the echo service
to return the text as is, but it should also print it and emit an event.

@TODO: think of a way to display `lymph emit` that is not confusing and doesn't harm flow.

``` shell
lymph request Echo.echo '{"text": "Good afternoon, EuroPython!"}'
```

The result of the RPC is as expected and the service printed the text.

This is boring and our service must be pretty lonely. Nobody listens to its
events. Here comes the ear.

[show Ear service code]

The ear listens to echo's events. Pardon the pun. Again, it's a lymph
service(we inherit from `lymph.Interface`). However, there's nothing but one
method which is subscribed to `echo` events. It simply prints the text contained
in the event's body. That means, everytime an event of this type occurs
exactly once instance of ear will consume it.

Let's excercise our services combination. This time round, though, we'll run
two instances of the echo service and one instance of the ear service.

``` shell
mux start echo-ear
```

Again, we see a tmux session. On the right you find two instances of the echo
service followed by an instance of the ear service.

We should find them registered correctly.

``` shell
lymph discover
```

And, indeed, they list correctly.

Let's emit an echo event in the event system to assert whether the ear service
listens to it. We'll use lymph's `emit` command. We're expecting the ear to
print the text field from the event body.

```
lymph emit echo '{"text": "hi"}'
```

Nice. That worked.

When we do RPCs now we expect the echo instances to respond in round-robin
fashion. Furthermore, the ear instance should print all consumed events.

``` shell
lymph request Echo.echo '{"text": "Good afternoon, EuroPython!"}'
```
(repeatedly, until both echo instances have responded)

As you see, our expectations are met.

If we were to run several instances of the ear services, each event would be
consumed by exactly once instance. However, lymph allows to broadcast events.

Finally, since it's 2015, let's add a web service to the mix. Let's say we
wanted to expose the echo functionality via an HTTP API. Lymph has a class for
that.

[show Web service code]

This is the Web service. It subclasses lymph's `WebServiceInterface`. In this
case we're not exposing RPC methods, emitting not listening to events. However,
we configure a Werkzeug URL map as a class attribute. We've added one endpoint:
`/echo` and a handler for it. The handler receives a Werkzeug reuqest object.

The echo handler unpacks the body of the request. It calls the echo service
via the `self.proxy` and returns the result in the response. And it prints.

Mind, that we're not validating the request method nor anything else.

Run it or it didn't happen. We'll bring up an instance of each of services now.

``` shell
mux start all
```

On the right you can see an instance of every service, Web, Echo and Ear.

Once again, they should have registered correctly:

``` shell
lymph discover
```

Let's hit our web service and see how the request ripples through our service
cluster. We should see all service print something. The web service is
listening at the default port 4080. We're using `httpie` to excercise the
request:

```
http localhost:4080/echo text=hi
```

The response looks good and all services have performed accordingly.

Yet, when developing locally you seldomly would want to run all of your
services within different shell or tmux panes. Lymph has its own development
server which wraps around any number of services with any number of instances
each. Therefore, we'll have to configure which services to run and how many
instances of each in the `.lymph.yml`:

``` yaml
instances:
    web:
        command: lymph instance --config=conf/web.yml

    echo:
        command: lymph instance --config=conf/echo.yml
        numprocesses: 3

    ear:
        command: lymph instance --config=conf/ear.yml
        numprocesses: 2
```

Mind that in our case `command` specifies lymph instances but this could also
be any other service you need, e.g. Redis.

Let's run it.

``` shell
mux start all
```

Once more, we find ourselves inside a tmux session with lymph node running in
the top-right pane. Below that you see lymph tail running which allows us to
follow the logs of any number of services. But first, let's check how many instances
are running:

``` shell
lymph discover
```

That's a good number. Once we feed a request into the cluster we should see print
statements and logs appearing.

``` shell
http localhost:4080/echo text=hi
```

But there's a lot going on. You would find an even bigger mess the more
services and instances you run and the more intricated your patterns of
communication become. Sometimes you wonder "where did my request go?". Lymph
helps you though with `trace\_id`s. Every request that appears in our cluster
which doesn't have a trace_id assigned gets one. These trace_ids get fowarded
via every RPC and event.

So we should be able to corellate all actions in cluster to the one incoming
HTTP request.

[use iterms highlighting: Ctrl+f and type 'trace_id']

And indeed we see the same trace_id across our service instances.

And that mostly covers the tooling we have for lymph services. Let's talk about
lymph's stack next.

## Lymph
...

## Flow notes
### Introduction
* Hello
* this is who we are
* company
* this is what we do
* what is this (what is lymph in a nutshell)
* why are we doing this (reasons)

### lymph
* sample (with local events and static registry)
 * introduce sample services / scenario
 * show them(code) and explain them
 * introduce echo
 * configure it
 * show tooling (run it, discover and inspect)
 * make a request
 * introduce listener
 * show tooling (run it, discover (and inspect))
 * (run more than one instance)
 * make a request
 * emit events, subscribe
 * introduce web
 * curl
 * show traceid in logs
* show sample with rabbitmq and zk
 * proves claim

### high-level architecture
* greenlets
* rpc via 0mq
* events via rabbitmq (pluggable)
* registry via zk (pluggable)
* http with werkzeug
* testing
* TestCases

### compare with nameko
* (http://lucumr.pocoo.org/2015/4/8/microservices-with-nameko/)
* tech
* running
* testing

### future
* eco system (storage, storeproxy, flow etc)
* distconfig

### summary and outro
* lymph.io
* we accept PRs
* we're hiring

### Q&A
* why zookeeper for registry?
* how to scale up web services? (sharing sockets)
 
### nice-to-have
* plugins (lymph-top, newrelic, sentry)
* monitoring
* serial events & broadcast(websockets)
* sieve of Erathostenes (Mislav)

