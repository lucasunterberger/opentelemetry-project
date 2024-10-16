'use strict'

const { LogLevel } = require("@opentelemetry/core")
const { NodeTraceProvider } = require("@opentelemetry/node")

const provider = new NodeTraceProvider({
    logLevel: LogLevel.ERROR
})

provider.register()

provider.addSpanProcessor(
    new SimpleSpanProcessor(
        new Zipkinexporter({
            serviceName: 'test-service'
        })
    )
)