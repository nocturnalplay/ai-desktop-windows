& "e:/mini project/mini/AI/ven/Scripts/Activate.ps1"

global install python package
`
python -m pip install opencv-python
`

`
cmd := exec.Command("cmd", "/C", "echo", "sdf")
	stdout, err := cmd.StdoutPipe()

	if err != nil {
		log.Fatal(err)
	}

	if err := cmd.Start(); err != nil {
		log.Fatal(err)
	}

	data, err := ioutil.ReadAll(stdout)

	if err != nil {
		log.Fatal(err)
	}

	if err := cmd.Wait(); err != nil {
		log.Fatal(err)
	}

	fmt.Printf("%s\n", data)
`