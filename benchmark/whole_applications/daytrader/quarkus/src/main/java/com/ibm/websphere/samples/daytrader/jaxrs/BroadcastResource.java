/**
 * (C) Copyright IBM Corporation 2019.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package com.ibm.websphere.samples.daytrader.jaxrs;

import java.util.List;

import jakarta.annotation.Priority;
import jakarta.enterprise.context.ApplicationScoped;
import jakarta.enterprise.event.ObservesAsync;
import jakarta.inject.Inject;
import jakarta.interceptor.Interceptor;
import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.Context;
import jakarta.ws.rs.core.MediaType;
import jakarta.ws.rs.sse.OutboundSseEvent.Builder;
import jakarta.ws.rs.sse.Sse;
import jakarta.ws.rs.sse.SseBroadcaster;
import jakarta.ws.rs.sse.SseEventSink;

import com.ibm.websphere.samples.daytrader.interfaces.QuotePriceChange;
import com.ibm.websphere.samples.daytrader.util.RecentQuotePriceChangeList;

@Path("broadcastevents")
@ApplicationScoped
public class BroadcastResource {

  private SseBroadcaster broadcaster;
  private Builder builder;

  @Context
  private Sse sse;

  @Inject RecentQuotePriceChangeList recentQuotePriceChangeList;

  @GET
  @Produces(MediaType.SERVER_SENT_EVENTS)
  public void register(@Context SseEventSink eventSink) {
    if (broadcaster == null && sse != null) {
      broadcaster = sse.newBroadcaster();
      builder = sse.newEventBuilder();
    }
    if (recentQuotePriceChangeList.isEmpty()) {
      eventSink.send(builder.data(new String("welcome!")).build());
    } else {
      eventSink.send(builder.mediaType(MediaType.APPLICATION_JSON_TYPE)
      .data(List.class,recentQuotePriceChangeList.recentList()).build());
    }
    broadcaster.register(eventSink);
  }

  public void eventStreamCdi(@ObservesAsync @Priority(Interceptor.Priority.APPLICATION + 1) @QuotePriceChange String event) {
    broadcaster.broadcast(builder.mediaType(MediaType.APPLICATION_JSON_TYPE)
        .data(List.class,recentQuotePriceChangeList.recentList()).build());

  }
}
