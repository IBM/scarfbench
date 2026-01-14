/*
 * Copyright (c), Eclipse Foundation, Inc. and its licensors.
 *
 * All rights reserved.
 *
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Distribution License v1.0, which is available at
 * https://www.eclipse.org/org/documents/edl-v10.php
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */
package jakarta.tutorial.custom_identity_store;

import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

@Service
public class TestIdentityStore implements UserDetailsService {

    @Override
    public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
        // This is for illustrative purposes only, and a real UserDetailsService should
        // include secure storage
        // and credential validation capabilities.
        // This example is a trivial one and is not meant to be used in production setup
        // at all. Use of
        // hard-coded/in-memory stores or user databases trivially provided as
        // unencrypted files etc is not
        // encouraged and has been used here in this manner just to demonstrate how a
        // custom identity
        // store can be defined.

        if ("Joe".equals(username)) {
            return User.builder()
                    .username("Joe")
                    .password("{noop}secret1") // {noop} means no password encoding
                    .roles("foo", "bar")
                    .build();
        }

        throw new UsernameNotFoundException("User not found: " + username);
    }
}
