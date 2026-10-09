# AI Vendor Assessment Addendum

Doc ID: AIV-STD
Version: 1.0
Owner: Chief Data and AI Officer
Effective: 2026-06-01
Status: Current

## 1. Purpose and Applicability

This addendum supplements DUE-STD for vendors that supply artificial intelligence or machine-learning services to Northwind. It applies when a vendor's service generates content, makes or recommends decisions, classifies or scores data, or uses a model trained or fine-tuned by the vendor or a fourth party. It applies equally to an AI feature added to an existing product; the Vendor Manager must notify the TPRM Office within 10 business days of learning that an existing vendor has enabled such a feature.

## 2. Minimum Tier

An AI vendor that processes Northwind Confidential data or personal data is Tier 2 at minimum. An AI vendor whose output is used in a decision about a client, such as credit, onboarding, fraud, or suitability, is Tier 1, regardless of spend.

## 3. Model Transparency

The vendor must disclose:

- the underlying model or models, the model provider (a fourth party under FRTH-POL where different from the vendor), and the version in use;
- the intended use and known limitations, normally as a model card or equivalent documentation;
- the categories of data used to train the model, at a level sufficient to assess bias and intellectual-property risk;
- where prompts, inputs, and outputs are processed and stored, and for how long.

The vendor must give at least 30 days' notice before a material model change, including a change of model provider, a major version upgrade, or a change in training data that affects Northwind's use case.

## 4. Use of Northwind Data for Training

Using Northwind data, including prompts, inputs, outputs, and feedback, to train, fine-tune, or otherwise improve the vendor's models or any third party's models is prohibited without prior written consent from the Northwind Data Owner and Legal. The prohibition must be written into the contract and the DPA (DPA-REQ clause 10). Consent, where given, must name the data set and purpose and may be withdrawn on 30 days' notice.

## 5. Human Oversight

Where AI output contributes to a decision affecting a client or an employee, the Business Owner must document the human review step, who performs it, and how reviewers can override the output. Fully automated decisions affecting clients require approval from the Chief Data and AI Officer and Legal.

## 6. Evaluation Evidence

Tier 1 and Tier 2 AI vendors provide evaluation evidence at onboarding and at least annually thereafter. Evidence must cover accuracy or quality metrics for Northwind's use case, bias and fairness testing across relevant groups, robustness testing including prompt-injection resistance for generative systems, and the results of red-team exercises. The Chief Data and AI Officer's team reviews this evidence alongside the CISO office's security review.

## 7. Harmful Output Incidents

The vendor must notify Northwind within 72 hours of becoming aware of harmful or materially incorrect output affecting Northwind, as set out in INCN-SLA. Harmful output includes discriminatory output, disclosure of another customer's data, fabricated facts presented as fact in a regulated communication, and output generated through a successful prompt-injection attack. Northwind employees who observe harmful output report it to the TPRM Office the same business day.

## 8. Logging

Vendors must make interaction logs for Northwind's use available to Northwind on request. Northwind's own retention of AI assistant interaction logs follows RET-SCH §3.

## 9. Exit

The exit plan must address retrieval of any Northwind-specific fine-tuned models, embeddings, or prompt libraries, and certified deletion of Northwind data from training pipelines (EXIT-PLN §4.2).
