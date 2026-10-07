# Before and after

These examples were written for this repository. They show what the skill changes and what it keeps.

## 1. An explanation (`explain`)

**Before**

> It's worth noting that when a JSON Web Token is being verified, the signature, which has been generated using the issuer's private key, is checked by the server against the public key that was previously obtained from the issuer's JWKS endpoint, and subsequently the `exp` claim is validated to ensure the token hasn't expired.

**After**

> The server verifies a JSON Web Token (JWT) in two steps.
>
> 1. The server checks the signature. The issuer made the signature with its private key. The server uses the public key from the issuer's JWKS endpoint.
> 2. The server reads the `exp` claim. If the time in `exp` is in the past, the server rejects the token.

Kept: `exp`, JWKS, "private key", "public key". Removed: "It's worth noting that", the passive verbs, "subsequently", "ensure".

## 2. An error message (`strict`)

**Before**

> Unfortunately the upload could not be completed, potentially owing to the file size exceeding the permitted maximum of 25 MB or the session having timed out.

**After**

> The upload did not complete. The file may be larger than the limit of 25 MB, or the session may have timed out. Make sure that the file is smaller than 25 MB. Then sign in and start the upload again.

The doubt is kept: "may be larger", "may have timed out". The number 25 MB is kept. The message has three parts: what occurred, the probable cause, what to do. The last part is new text. Add it only when you know the correct action.

## 3. A tool description for an AI agent (`strict`)

**Before**

> Searches the knowledge base and returns relevant results; results are ranked and may be truncated when the limit parameter is exceeded, with the default being 10 if nothing is specified.

**After**

> The tool searches the knowledge base.
> The tool returns the results in order of relevance.
> The `limit` parameter sets the maximum number of results.
> If the caller does not set `limit`, the tool uses 10.
> If there are more results than `limit`, the tool returns only the first `limit` results.

Each sentence names the actor. Each condition and the default value are stated. The semicolon is gone.

## 4. A procedure (`rewrite`)

**Before**

> Before the migration is run you'll want to make sure a backup has been taken, then the app should be put into maintenance mode, the migration script executed, and finally check that the row counts match prior to switching maintenance mode off.

**After**

> CAUTION: Make a backup before you start the migration.
>
> 1. Put the app into maintenance mode.
> 2. Run the migration script.
> 3. Compare the row counts before and after the migration.
> 4. If the row counts are equal, set maintenance mode to off.

## 5. A fact that a strict rewrite loses

**Source**

> The function debounces the resize handler by 200 ms.

**Too strict (incorrect)**

> The function waits before it does the work again.

**80% STE (correct)**

> The function debounces the resize handler by 200 ms. "Debounce" means: wait until the events stop, then run the handler one time.

The checker finds the loss:

```
$ python skills/ste-explain/scripts/ste_check.py --compare source.md strict.md
compare: 1 hard, 0 advisory
  HARD     lost-fact: "200 ms" is in the source and not in the rewrite
strict.md: 0 hard, 0 advisory
```

The style check passes and the fact check fails. Short sentences are not sufficient.
