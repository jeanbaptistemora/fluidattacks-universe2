tls1_process_heartbeat(SSL *s)
3966  {
3967  unsigned char *p = &s->s3->rrec.data[0], *pl;
3968  unsigned short hbtype;
3969  unsigned int payload;
3970  unsigned int padding = 16; /* Use minimum padding */
3971
3972  /* Read type and payload length first */
3973  hbtype = *p++;
3974  n2s(p, payload);
3975  pl = p;
3976
3977  if (s->msg_callback)
3978    s->msg_callback(0, s->version, TLS1_RT_HEARTBEAT,
3979      &s->s3->rrec.data[0], s->s3->rrec.length,
3980      s, s->msg_callback_arg);
3981
3982    if (hbtype == TLS1_HB_REQUEST)
3983    {
3984      unsigned char *buffer, *bp;
3985      int r;
3986
3987      /* Allocate memory for the response, size is 1 bytes
3988      * message type, plus 2 bytes payload length, plus
3989      * payload, plus padding
3990      */
3991      buffer = OPENSSL_malloc(1 + 2 + payload + padding);
3992      bp = buffer;
3993
3994      /* Enter response type, length and copy payload */
3995      bp++ = TLS1_HB_RESPONSE;
3996      s2n(payload, bp);
3997      memcpy(bp, pl, payload);
3998      bp += payload;
3999      /* Random padding */
4000      RAND_pseudo_bytes(bp, padding);
