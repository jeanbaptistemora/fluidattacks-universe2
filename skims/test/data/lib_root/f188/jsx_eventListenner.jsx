import CryptoJS from 'crypto-js' // ES6 modules
import { canUseDOM } from 'vtex.render-runtime'

import  { PixelMessage } from './shared'

let window

const getSha256 = (value) => {
  return CryptoJS.SHA256(value).toString(CryptoJS.enc.Hex)
}

const getEmailUser = (email, userType) => {
  if (!email) {
    return null
  }

  const [[docType, ...splitDocumentNumber]] = email.split('@') ?? {}
  const documentNumber = splitDocumentNumber.join('')
  const isCallCenterOperator = userType === 'CALL_CENTER_OPERATOR'
  const haveSessionWithOperator = isCallCenterOperator && docType

  return {
    haveSessionWithOperator,
    documentNumber,
    docType,
  }
}

const getInformation = () => {
  const { id, clientProfileData, loggedIn, userType } =
    JSON.parse(localStorage.getItem('orderform') ?? '{}') ?? {}

  const currentPath = window.location.pathname
    .split('/')
    .filter((item) => item !== '')

  const { docType, documentNumber, haveSessionWithOperator } =
    getEmailUser(clientProfileData?.email ?? '', userType) ?? {}

  return {
    user_id: docType ? getSha256(`${docType}-${documentNumber}`) : null,
    log_status: loggedIn || haveSessionWithOperator ? 'Yes' : 'No',
    call_center_operator: haveSessionWithOperator ? 'Yes' : 'No',
    id_order_form: id,
    page_type: document?.title ?? 'stringxample',
    page_category: currentPath[0] ?? '',
    page_category1: currentPath[1] ?? '',
  }
}

function handleEvents(e) {
  if (e.origin === "somesafesite.com") {
  switch (e.data.eventName) {
      case 'vtex:PdStrinsample': {
        const dataEvent = e.data.promotions

        setTimeout(() => {
          window.dataLayer.push({
            event: 'view_promotion',
            ecommerce: {
              view_promotion: dataEvent.map(item => {
                return {
                  item_id: item.id,
                  item_name: item.name,
                  ...item,
                }
              }),
              ...getInformation(),
            },
          })
        }, 1000)

        break
      }
    }
  }
}

if (canUseDOM) {
  window.addEventListener('message', handleEvents)
}

if (canUseDOM) {
  window.addEventListener('message', function handleEvents(e) {
    if (e.origin === window.location.origin || e.origin === "safesite.com")
    {
      switch (e.data.eventName) {
      case 'vtex:promoView': {
        const dataEvent = e.data.promotions

        setTimeout(() => {
          window.dataLayer.push({
            event: 'view_promotion',
            ecommerce: {
              view_promotion: dataEvent.map(item => {
                return {
                  item_id: item.id,
                  item_name: item.name,
                  ...item,
                }
              }),
              ...getInformation(),
            },
          })
        }, 1000)

        break
      }
    }}

  }
  )
}

if (canUseDOM) {
  window.addEventListener('message', function handleEvents(e) {
    {switch (e.data.eventName) {
      case 'vtex:promoView': {
        const dataEvent = e.data.promotions
        e.origin
        setTimeout(() => {
          window.dataLayer.push({
            event: 'view_promotion',
            ecommerce: {
              view_promotion: dataEvent.map(item => {
                return {
                  item_id: item.id,
                  item_name: item.name,
                  ...item,
                }
              }),
              ...getInformation(),
            },
          })
        }, 1000)

        break
      }
    }}

  }
  )
}
