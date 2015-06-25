(http://socrates.io/#xfL9riN)

# Stop trying to glue your services together`; import lymph`

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
* We're going to explain where we're coming from and why we have given birth to another framework
* We'll look at code as fast possible
* We'll run services and increasingly add new services to explore communication patterns and characteristics of lymph
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
light of a global platform to unite our very heterogenix Product landscape.

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

[Show simple echo service]

One of the first things we considered when building lymph was the tooling. We
think we managed to get some very nice tooling built around it to make
development of services easier.

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

### QA
 
### nice-to-have
* plugins (lymph-top, newrelic, sentry)
* monitoring
* serial events & broadcast(websockets)

# Setup

create virtualenv:
```
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt
```

install tmuxinator:
```
brew install tmuxinator
```

make sure `$EDITOR` is set:
```
mux doctor
```

link tmuxinator projects:
```
ln -s `pwd`/tmuxinator/* ~/.tmuxinator
```

remove zookeeper node `/lymph`:
```
zkCli.sh
rmr /lymph
```

make sure zk and rabbitmq are running. start tmuxinator project:
```
mux start all
```
