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
package com.ibm.websphere.samples.daytrader.impl.ejb3;

import java.time.Duration;
import java.util.concurrent.Future;

import io.smallrye.mutiny.Uni;
import jakarta.enterprise.context.RequestScoped;
import jakarta.inject.Inject;

@RequestScoped
public class AsyncScheduledOrderSubmitter {
  
  
  // @Resource
  // private ManagedScheduledExecutorService mes;
  

  @Inject
  private AsyncScheduledOrder asyncOrder;
  
  
  public Future<?> submitOrder(Integer orderID, boolean twoPhase) {
    asyncOrder.setProperties(orderID,twoPhase);
    // return scheduler.schedule(asyncOrder,500,TimeUnit.MILLISECONDS);
    return Uni.createFrom().item(asyncOrder)
                   .onItem().delayIt().by(Duration.ofMillis(500))
                   .onItem().invoke(Runnable::run)
                   .subscribeAsCompletionStage(); // converts to CompletableFuture<?>
  }
}
