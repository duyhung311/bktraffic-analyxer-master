# Inference


* **URL**

  /inference

* **Method:**

  `POST`
  
*  **URL Params**

    None

* **Data Params**

   **Required:**
    ```yaml
    segment_id: List[integer]
    timestamps: List[integer] | integer
    ```

* **Success Response:**

  * **Code:** 200

    **Params:**
    ``` yaml
    {
      segment_id: [1, 2, 3],
      timestamp: 123456
    }
    ```

    **Content:**
    ``` yaml
    {
      code: 200,
      message: "",
      data: {
        segment_id: [1, 2, 3],
        velocity: [40, 30, 20],
        LOS: ["40", "30", "20"],
      },
      errors: [],
      debugError: []
    }
    ```
  
    **Params:**
    ``` yaml
    {
      segment_id: [1, 2, 3],
      timestamp: [123456, 123457]
    }
    ```
    **Content:**
    ``` yaml
    {
      code: 200,
      message: "",
      data: {
        period_1_25: {
          segment_id: [1, 2, 3],
          velocity: [40, 30, 20],
          LOS: ["40", "30", "20"],
        },
        period_1_30: {
          segment_id: [1, 2, 3],
          velocity: [40, 30, 20],
          LOS: ["40", "30", "20"],
        }
      },
      errors: [],
      debugError: []
    }
    ```
 
* **Error Response:**

  * **Code:** 400 BAD REQUEST

    **Content:**
    ``` yaml
    {
      code: 400,
      message: "",
      data: {},
      errors: [
        {
          domain: "field_abc",
          reason: "wrong data type",
          message: "Field abc is not in the right data type"
        }
      ],
      debugError: []
    }
    ```

  OR

  * **Code:** 500 INTERNAL SERVER ERROR

    **Content:**
    ``` yaml
    {
      code: 500,
      message: "",
      data: {},
      errors: [],
      debugError: []
    }
    ```

* **Sample Call:**
