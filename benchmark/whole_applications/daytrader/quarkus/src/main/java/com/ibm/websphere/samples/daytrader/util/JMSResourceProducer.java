package com.ibm.websphere.samples.daytrader.util;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.inject.Produces;
import jakarta.inject.Singleton;
import jakarta.jms.ConnectionFactory;
import jakarta.jms.JMSContext;
import jakarta.jms.Queue;
import jakarta.jms.QueueConnectionFactory;
import jakarta.jms.Topic;
import jakarta.jms.TopicConnectionFactory;

import org.apache.activemq.artemis.jms.client.ActiveMQConnectionFactory;
import org.apache.activemq.artemis.jms.client.ActiveMQQueue;
import org.apache.activemq.artemis.jms.client.ActiveMQTopic;

/**
 * CDI Producer bean for JMS resources in Quarkus.
 * Provides QueueConnectionFactory, TopicConnectionFactory, Queue, and Topic beans.
 */
@ApplicationScoped
public class JMSResourceProducer {

    private static final String BROKER_URL = "tcp://localhost:61616";
    private static final String BROKER_USERNAME = "admin";
    private static final String BROKER_PASSWORD = "admin";
    
    private JMSContext jmsContext;

    /**
     * Produces QueueConnectionFactory bean
     */
    @Produces
    @Singleton
    public QueueConnectionFactory produceQueueConnectionFactory() {
        return (QueueConnectionFactory) new ActiveMQConnectionFactory(BROKER_URL, BROKER_USERNAME, BROKER_PASSWORD);
    }

    /**
     * Produces TopicConnectionFactory bean
     */
    @Produces
    @Singleton
    public TopicConnectionFactory produceTopicConnectionFactory() {
        return (TopicConnectionFactory) new ActiveMQConnectionFactory(BROKER_URL, BROKER_USERNAME, BROKER_PASSWORD);
    }

    /**
     * Produces JMSContext bean - lazily creates context on first access
     */
    @Produces
    public JMSContext produceJMSContext() {
        if (jmsContext == null) {
            try {
                ConnectionFactory cf = new ActiveMQConnectionFactory(BROKER_URL, BROKER_USERNAME, BROKER_PASSWORD);
                jmsContext = cf.createContext();
            } catch (Exception e) {
                Log.error("Failed to create JMSContext: " + e.getMessage(), e);
                // Return null to allow application to continue without JMS
                return null;
            }
        }
        return jmsContext;
    }

    /**
     * Produces TradeBrokerQueue bean
     */
    @Produces
    @Singleton
    @TradeBrokerQueue
    public Queue produceTradeBrokerQueue() {
        return new ActiveMQQueue("jms/TradeBrokerQueue");
    }

    /**
     * Produces TradeUpdatesTopic bean
     */
    @Produces
    @Singleton
    @TradeUpdatesTopic
    public Topic produceTradeUpdatesTopic() {
        return new ActiveMQTopic("jms/TradeUpdatesTopic");
    }

    /**
     * Produces TradeStreamerTopic bean
     */
    @Produces
    @Singleton
    @TradeStreamerTopic
    public Topic produceTradeStreamerTopic() {
        return new ActiveMQTopic("jms/TradeStreamerTopic");
    }
}
