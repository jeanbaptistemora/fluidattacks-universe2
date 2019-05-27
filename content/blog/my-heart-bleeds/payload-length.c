/* Read type and payload length first */
3972         /* Read type and payload length first */
3973         hbtype = *p++;
3974         n2s(p, payload);
3975         pl = p;
