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

import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

/**
 * Test REST Controller that prints out the name of the authenticated caller and
 * whether
 * this caller is in any of the roles {foo, bar, kaz}
 *
 */

@RestController
public class Servlet {

    @GetMapping("/servlet")
    public String getUser(Authentication authentication) {
        StringBuilder response = new StringBuilder();

        String webName = null;
        if (authentication != null) {
            webName = authentication.getName();
        }

        response.append("web username: ").append(webName).append("\n");

        response.append("web user has role \"foo\": ").append(hasRole(authentication, "foo")).append("\n");
        response.append("web user has role \"bar\": ").append(hasRole(authentication, "bar")).append("\n");
        response.append("web user has role \"kaz\": ").append(hasRole(authentication, "kaz")).append("\n");

        return response.toString();
    }

    private boolean hasRole(Authentication authentication, String role) {
        if (authentication == null) {
            return false;
        }
        return authentication.getAuthorities().stream()
                .map(GrantedAuthority::getAuthority)
                .anyMatch(auth -> auth.equals("ROLE_" + role));
    }
}
