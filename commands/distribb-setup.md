---
description: Set up Distribb - check API key, confirm website + GSC are connected, enable the slash commands
argument-hint: (none)
allowed-tools: Bash, Read, Write, Glob, Grep, WebFetch
---

Load the Distribb skill (`.claude/skills/distribb/` or `~/.claude/skills/distribb/`) and run setup:

1. **API key.** Confirm `DISTRIBB_API_KEY` is set and works: `curl -s -H "Authorization: Bearer $DISTRIBB_API_KEY" https://distribb.io/api/v1/projects`. If missing/invalid, tell the user to get it from Settings at https://distribb.io (after signing up and completing onboarding).

2. **Onboarding.** Confirm the project exists and key fields are filled (`GET /api/v1/business-context`): business description, competitors (3-7), content pillars, AI instructions. If thin, offer to improve them. See `references/onboarding-guide.md`.

3. **Website / CMS.** `GET /api/v1/integrations` - confirm a CMS is connected so Distribb can publish. Also confirm the site has a blog to publish to.

4. **Google Search Console.** `GET /api/v1/search-console` - if `connected:false`, send the user to https://distribb.io/integrations . If they do not have Search Console at all, point them to https://support.google.com/webmasters/answer/10267942?hl=en first.

5. **Register the slash commands.** Locate this skill's `commands/` folder and copy the command files into the project so they work as `/` commands:
   ```bash
   mkdir -p .claude/commands && cp <skill_dir>/commands/*.md .claude/commands/
   ```
   Confirm to the user which commands are now available.

6. Finish by showing the proper SEO process and recommending they run `/gsc-audit <their-domain>` next.
