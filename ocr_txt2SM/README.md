# ver1 code

## /extractors\_ver1
Contains the extractors.

- callFlowExtractor.py extracts callFlows from RFCs
- messageStructureExtractor.py extracts messages structures from RFCs
- messageStructureReader.py is to transform the message structures into json objects
- textExtractor.py is to extract text from images

## /example\_images\_ver1
Contains several images and screenshots used in the paper

## /packetTracesAnalysis_ver1
- Contains the script to analyse the packet traces: packetTracesAnalysis.py
- We worked with datasets available here: https://archive.wrccdc.org/pcaps/
- Contains a file with the source and destination ports for the messages in the dataset wrccdc.2018-03-23.010014000000000.pcap

Tip: To cut a pcap file use:
`tcpdump -r old_file -w new_files -C 10`
(Here it cuts it in 10 million bytes files)

## /box\_extraction
currently contains scripts to extract entity boxes from artifacts that contain them
